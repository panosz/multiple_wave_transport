#include "multiple_wave_system.hpp"
#include <boost/math/constants/constants.hpp>
#include <boost/numeric/odeint/stepper/generation/make_controlled.hpp>
#include <cmath>
#include <iostream>
#include "helper_collections.hpp"
#include <boost/numeric/odeint.hpp>
#include <boost/numeric/odeint/external/eigen/eigen.hpp>

namespace WP {

void ThreeWaveSystem::operator()(const State &s, State &dsdt,
                                 double t) const noexcept {
  using namespace boost::math::double_constants;
  const auto &x = s[0];
  const auto &p = s[1];

  dsdt[0] = p;
  const auto t_times_two_pi = t * two_pi;
  const auto pert = -cos(t_times_two_pi - x) - cos(2 * t_times_two_pi - x) -
                    cos(3 * t_times_two_pi - x);
  dsdt[1] = epsilon * pert;
}

State ThreeWaveSystem::call(const State &s, double t) const noexcept {
  State dsdt{2, 3};
  this->operator()(s, dsdt, t);
  return dsdt;
}
OrbitPoints ThreeWaveSystem::repeat_state(const State &s) const noexcept {
  WP::collections::OrbitStdVector out{};

  for (int i = 0; i < 4; i++)
    out.push_back(i*s);
  return out;
}

class PushBackStateObesrver
{
    WP::collections::OrbitStdVector& m_states;
  public:
    PushBackStateObesrver( WP::collections::OrbitStdVector& states )
    : m_states( states ) { }

    void operator()( const WP::State& x, double /*t*/) 
    {
        m_states.push_back( x );
    }
};


OrbitPoints ThreeWaveSystem::poincare(const State &s, double t_max) const noexcept {
  WP::collections::OrbitStdVector out{};

  using namespace boost::numeric::odeint;
  typedef boost::numeric::odeint::runge_kutta_dopri5<State> stepper_type;

  const double atol = 1.0e-10;
  const double rtol = 1.0e-10;

  auto stepper = make_dense_output( atol , rtol , stepper_type() );

  State s_cur = s;

  integrate_const(stepper, *this, s_cur, 0.0, t_max, 1., PushBackStateObesrver(out));
  return out;
}

template<typename DenseStepper>
double track_down_cross_time(DenseStepper &stepper, double p_max) {
  // improve accuracy of the crossing time by bisection method
  // It is assumed that the event is detected at the last step taken by the stepper

  double t2 = stepper.current_time();
  double dt = stepper.current_time_step();
  double t1 = t2 - dt;

  double t = (t1 + t2) / 2;  // start with the midpoint
  State x;

  while (t2 - t1 > 1e-5) {  // until the precision is high enough
    stepper.calc_state(t, x);  // interpolate the state at time t
    if (x[1] > p_max) {
      t2 = t;  // if the event is detected, the time is too late
    } else {
      t1 = t;  // if no event is detected, the time is too early
    }
    t = (t1 + t2) / 2;  // update the time
    }
  return t;
}


double ThreeWaveSystem::get_loss_time(const State &s_init, double p_max, double t_max) const noexcept {

  using namespace boost::numeric::odeint;

  typedef boost::numeric::odeint::runge_kutta_dopri5<State> stepper_type;
  const double atol = 1.0e-10;
  const double rtol = 1.0e-10;
  const double dt_init = 1.0e-3;

  if (s_init[1] > p_max) {
    return 0.0;
  }

  //
  auto stepper = make_dense_output(atol, rtol, stepper_type());

  State s_cur = s_init;

  const auto begin = make_adaptive_time_iterator_begin(std::ref(stepper), *this, s_cur, 0.0, t_max, dt_init);
  const auto end = make_adaptive_time_iterator_end(std::ref(stepper), *this, s_cur);

  for (auto it = begin; it != end; ++it) {
    const auto &s = it->first;
    if (s[1] > p_max) {
      return track_down_cross_time(stepper, p_max);
    }
  }
  return t_max;
}

} // namespace WP
