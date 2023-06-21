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

double ThreeWaveSystem::get_loss_time(const State &s_init, double p_max, double t_max) const noexcept {

  using namespace boost::numeric::odeint;

  typedef boost::numeric::odeint::runge_kutta_dopri5<State> stepper_type;
  const double atol = 1.0e-10;
  const double rtol = 1.0e-10;
  const double dt_init = 1.0e-3;

  if (s_init[1] > p_max) {
    return 0.0;
  }

  // use controlled output stepper
  // use boost adaptive step time iterators
  //
  auto stepper = make_controlled(atol, rtol, stepper_type());

  State s_cur = s_init;

  const auto begin = make_adaptive_time_iterator_begin(stepper, *this, s_cur, 0.0, t_max, dt_init);
  const auto end = make_adaptive_time_iterator_end(stepper, *this, s_cur);

  for (auto it = begin; it != end; ++it) {
    const auto &s = it->first;
    const auto &t = it->second;
    if (s[1] > p_max) {
      return t;
    }
  }
  return t_max;
}

} // namespace WP
