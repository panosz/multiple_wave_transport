#include "perturbed_pendulum.hpp"
#include "helper_collections.hpp"
#include <boost/math/constants/constants.hpp>
#include <boost/numeric/odeint.hpp>
#include <boost/numeric/odeint/external/eigen/eigen.hpp>
#include <boost/numeric/odeint/stepper/generation/make_controlled.hpp>
#include <cmath>
#include <iostream>

namespace WP {

void UnperturbedPendulum::operator()(const State &s, State &dsdt,
                                     double /*t*/) const noexcept {
  using namespace boost::math::double_constants;
  const auto &x = s[0];
  const auto &p = s[1];

  dsdt[0] = p;
  dsdt[1] = sin(x);
}

double UnperturbedPendulum::energy(const State &s) const noexcept {
  using namespace boost::math::double_constants;
  const auto &x = s[0];
  const auto &p = s[1];

  return 0.5 * p * p + cos(x);
}

State UnperturbedPendulum::integrate(const State &s, double t) const noexcept {
  using namespace boost::numeric::odeint;
  typedef boost::numeric::odeint::runge_kutta_dopri5<State> stepper_type;
  using namespace boost::math::double_constants;

  const double atol = 1.0e-10;
  const double rtol = 1.0e-10;

  auto stepper = make_controlled(atol, rtol, stepper_type());

  State s_cur = s;
  const auto dt_init = 0.01;

  integrate_adaptive(stepper, *this, s_cur, 0.0, t, dt_init);

  return s_cur;
}

class PushBackStateObesrver {
  WP::collections::OrbitStdVector &m_states;

public:
  PushBackStateObesrver(WP::collections::OrbitStdVector &states)
      : m_states(states) {}

  void reserve(size_t n) { m_states.reserve(n); }
  void operator()(const WP::State &x, double /*t*/) { m_states.push_back(x); }
};

template <typename System>
OrbitPoints poincare_impl(const System &sys, const State &s, double t_max,
                          double delta_t) noexcept {
  WP::collections::OrbitStdVector out{};

  using namespace boost::numeric::odeint;
  typedef boost::numeric::odeint::runge_kutta_dopri5<State> stepper_type;
  using namespace boost::math::double_constants;

  const double atol = 1.0e-9;
  const double rtol = 1.0e-9;

  auto stepper = make_controlled(atol, rtol, stepper_type());

  State s_cur = s;

  auto observer = PushBackStateObesrver(out);
  observer.reserve(static_cast<size_t>(std::ceil(t_max / delta_t)));

  integrate_const(stepper, sys, s_cur, 0.0, t_max, delta_t,
                  observer);
  return out;
}

bool is_outside_X(const State &s) {
  using namespace boost::math::double_constants;
  return (s[0] > two_pi) || (s[0] < 0.0);
}

bool is_outside_P(const State &s) { return (s[1] > 2.01) || (s[1] < -2.01); }

template <typename DenseStepper>
double track_down_cross_time(DenseStepper &stepper,
                             bool (*is_outside)(const State &)) {
  // improve accuracy of the crossing time by bisection method
  // It is assumed that the event is detected at the last step taken by the
  // stepper

  double t2 = stepper.current_time();
  double dt = stepper.current_time_step();
  double t1 = t2 - dt;

  double t = (t1 + t2) / 2; // start with the midpoint
  State x;

  while (t2 - t1 > 1e-5) {    // until the precision is high enough
    stepper.calc_state(t, x); // interpolate the state at time t
    if (is_outside(x)) {
      t2 = t; // if the event is detected, the time is too late
    } else {
      t1 = t; // if no event is detected, the time is too early
    }
    t = (t1 + t2) / 2; // update the time
  }
  return t;
}

auto get_boundary_check_function(WP::BoundaryType boundarytype) {
  switch (boundarytype) {
  case WP::BoundaryType::X:
    return is_outside_X;
  case WP::BoundaryType::P:
    return is_outside_P;
  default:
    throw std::runtime_error("Unknown boundary type");
  }
}

template <typename System>
double get_loss_time_impl(const System &sys, const State &s_init, double t_max,
                          WP::BoundaryType boundarytype) noexcept {
  auto is_outside = get_boundary_check_function(boundarytype);

  using namespace boost::numeric::odeint;

  typedef boost::numeric::odeint::runge_kutta_dopri5<State> stepper_type;
  const double atol = 1.0e-10;
  const double rtol = 1.0e-10;
  const double dt_init = 1.0e-3;

  if (is_outside_X(s_init)) {
    return 0.0;
  }

  // use controlled output stepper
  // use boost adaptive step time iterators
  //
  auto stepper = make_dense_output(atol, rtol, stepper_type());

  State s_cur = s_init;

  const auto begin = make_adaptive_time_iterator_begin(
      std::ref(stepper), sys, s_cur, 0.0, t_max, dt_init);
  const auto end =
      make_adaptive_time_iterator_end(std::ref(stepper), sys, s_cur);

  for (auto it = begin; it != end; ++it) {
    const auto &s = it->first;
    if (is_outside(s)) {
      return track_down_cross_time(stepper, is_outside);
    }
  }
  return t_max;
}

inline void PerturbedPendulum::operator()(const State &s, State &dsdt,
                                   double t) const noexcept {
  using namespace boost::math::double_constants;
  const auto &x = s[0];
  const auto &p = s[1];

  dsdt[0] = p;
  dsdt[1] = sin(x) - epsilon * cos(5 * x - t / 2);
}

State PerturbedPendulum::call(const State &s, double t) const noexcept {
  State dsdt{2, 3};
  this->operator()(s, dsdt, t);
  return dsdt;
}

OrbitPoints PerturbedPendulum::poincare(const State &s,
                                        double t_max) const noexcept {

  return poincare_impl(*this, s, t_max, poincare_dt);
}

double
PerturbedPendulum::get_loss_time(const State &s_init, double t_max,
                                 WP::BoundaryType boundarytype) const noexcept {
  return get_loss_time_impl(*this, s_init, t_max, boundarytype);
}

inline void PerturbedPendulumWithLowFrequency::operator()(const State &s, State &dsdt,
                                                   double t) const noexcept {
  using namespace boost::math::double_constants;
  const auto &x = s[0];
  const auto &p = s[1];

  constexpr double low_omega = 0.05;

  dsdt[0] = p;
  dsdt[1] = sin(x) - epsilon_high * cos(5 * x - t / 2) -
            epsilon_low * cos(x - t * low_omega);
}

State PerturbedPendulumWithLowFrequency::call(const State &s,
                                              double t) const noexcept {
  State dsdt{2, 3};
  this->operator()(s, dsdt, t);
  return dsdt;
}

OrbitPoints
PerturbedPendulumWithLowFrequency::poincare(const State &s,
                                            double t_max) const noexcept {

  return poincare_impl(*this, s, t_max, poincare_dt);
}

double PerturbedPendulumWithLowFrequency::get_loss_time(
    const State &s_init, double t_max,
    WP::BoundaryType boundarytype) const noexcept {
  return get_loss_time_impl(*this, s_init, t_max, boundarytype);
}

} // namespace WP
