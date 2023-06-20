#ifndef WP_TYPES_INCLUDED
#define WP_TYPES_INCLUDED
#include <Eigen/Core>
#include <vector>

namespace WP{
  typedef Eigen::ArrayXd Vector;
  typedef Eigen::Vector2d State;
  typedef Eigen::Array2Xd OrbitPoints;
}

#endif //WP_TYPES_INCLUDED
