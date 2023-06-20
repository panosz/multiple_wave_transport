#ifndef WP_HELPER_COLLECTIONS_UTI1AEGH
#define WP_HELPER_COLLECTIONS_UTI1AEGH

#include "type_definitions.hpp"
#include <vector>

namespace WP {
namespace collections {
class OrbitStdVector : public std::vector<State> {
public:
  operator OrbitPoints() const;
};
} // namespace collections
} // namespace WP

#endif // WP_HELPER_COLLECTIONS_UTI1AEGH
