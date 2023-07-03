#ifndef PERTURBED_PENDULUM_AU7HOOCA
#define PERTURBED_PENDULUM_AU7HOOCA
#include "type_definitions.hpp"

namespace WP {

enum class BoundaryType {X, P};

class UnperturbedPendulum {
public:
  void operator()(const State &s, State &dsdt, double t) const noexcept;
  State integrate(const State &s, double t) const noexcept;
  double energy(const State &s) const noexcept;

};

class PerturbedPendulum {
  double epsilon;

public:
  explicit PerturbedPendulum(double _epsilon) noexcept : epsilon(_epsilon){};
  State call(const State &s, double t) const noexcept;
  void operator()(const State &s, State &dsdt, double t) const noexcept;
  OrbitPoints repeat_state(const State &s) const noexcept;
  OrbitPoints poincare(const State &s, double t_max) const noexcept;
  double get_loss_time(const State &s_init, double t_max, BoundaryType b=BoundaryType::X) const noexcept;
  /**
   * @brief      Calculate the time it takes for a single state to reach the
   * "loss region" p>p_max or t>t_max.
   *
   *           The loss region is defined as the region where the state is no
   * longer in the "confined" domain. This is done by integrating the state
   * until it reaches the loss region. The time it takes to reach the loss
   * region is returned. If the state does not reach the loss region, t_max is
   * returned. If the state is already in the loss region, 0 is returned.
   *
   *
   * @param[in]  s_init  The initial state
   * @param[in]  t_max   The maximum integration time
   * @param[in]  dt      The initial time step
   * @return     The time it takes to reach the loss region
   */
};

class PerturbedPendulumWithLowFrequency {
  double epsilon_high;
  double epsilon_low;

public:
  PerturbedPendulumWithLowFrequency(double _epsilon_high, double _epsilon_low) noexcept : epsilon_high(_epsilon_high), epsilon_low(_epsilon_low){};
  State call(const State &s, double t) const noexcept;
  void operator()(const State &s, State &dsdt, double t) const noexcept;
  OrbitPoints repeat_state(const State &s) const noexcept;
  OrbitPoints poincare(const State &s, double t_max) const noexcept;
  double get_loss_time(const State &s_init, double t_max, BoundaryType b=BoundaryType::X) const noexcept;
  /**
   * @brief      Calculate the time it takes for a single state to reach the
   * "loss region" p>p_max or t>t_max.
   *
   *           The loss region is defined as the region where the state is no
   * longer in the "confined" domain. This is done by integrating the state
   * until it reaches the loss region. The time it takes to reach the loss
   * region is returned. If the state does not reach the loss region, t_max is
   * returned. If the state is already in the loss region, 0 is returned.
   *
   *
   * @param[in]  s_init  The initial state
   * @param[in]  t_max   The maximum integration time
   * @param[in]  dt      The initial time step
   * @return     The time it takes to reach the loss region
   */

};

class PerturbedPendulumOnlyLowFrequency {
  double epsilon;

public:
  explicit PerturbedPendulumOnlyLowFrequency(double _epsilon) noexcept : epsilon(_epsilon){};
  State call(const State &s, double t) const noexcept;
  void operator()(const State &s, State &dsdt, double t) const noexcept;
  OrbitPoints repeat_state(const State &s) const noexcept;
  OrbitPoints poincare(const State &s, double t_max) const noexcept;
  double get_loss_time(const State &s_init, double t_max, BoundaryType b=BoundaryType::X) const noexcept;
  /**
   * @brief      Calculate the time it takes for a single state to reach the
   * "loss region" p>p_max or t>t_max.
   *
   *           The loss region is defined as the region where the state is no
   * longer in the "confined" domain. This is done by integrating the state
   * until it reaches the loss region. The time it takes to reach the loss
   * region is returned. If the state does not reach the loss region, t_max is
   * returned. If the state is already in the loss region, 0 is returned.
   *
   *
   * @param[in]  s_init  The initial state
   * @param[in]  t_max   The maximum integration time
   * @param[in]  dt      The initial time step
   * @return     The time it takes to reach the loss region
   */
};

} // namespace WP

#endif // end of include guard: PERTURBED_PENDULUM_AU7HOOCA

