#ifndef MULTIPLE_WAVE_SYSTEM_IEY4EIL5
#define MULTIPLE_WAVE_SYSTEM_IEY4EIL5
#include "type_definitions.hpp"

namespace WP {
class ThreeWaveSystem {
  double epsilon;

public:
  explicit ThreeWaveSystem(double _epsilon) noexcept : epsilon(_epsilon){};
  State call(const State &s, double t) const noexcept;
  void operator()(const State &s, State &dsdt, double t) const noexcept;
  OrbitPoints repeat_state(const State &s) const noexcept;
  OrbitPoints poincare(const State &s, double t_max) const noexcept;
  double get_loss_time(const State &s_init, double p_max, double t_max) const noexcept;
  /**
  * @brief      Calculate the time it takes for a single state to reach the "loss region" p>p_max
  *            or t>t_max.
  *           
  *           The loss region is defined as the region where the state is no longer in the "confined" domain.
  *           This is done by integrating the state until it reaches the loss region.
  *           The time it takes to reach the loss region is returned.
  *           If the state does not reach the loss region, t_max is returned.
  *           If the state is already in the loss region, 0 is returned.
  *
  *
  * @param[in]  s_init  The initial state
  * @param[in]  p_max   The maximum value of p allowed
  * @param[in]  t_max   The maximum integration time
  * @param[in]  dt      The initial time step
  * @return     The time it takes to reach the loss region
  */

};
} // namespace WP

#endif // end of include guard: MULTIPLE_WAVE_SYSTEM_IEY4EIL5
