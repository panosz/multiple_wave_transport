#include "helper_collections.hpp"

using namespace WP::collections;

OrbitStdVector::operator OrbitPoints() const {
  WP::OrbitPoints out(4, size());
  for (long unsigned i = 0; i < size(); i++)
    out.col(i) = (*this)[i];
  return out;
}
