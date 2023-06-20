cmake_minimum_required(VERSION 3.15...3.19)
include(CMakePrintHelpers)

project(scikit_build_example VERSION "0.0.1")

set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

# if(SKBUILD)
  # Scikit-Build does not add your site-packages to the search path
  # automatically, so we need to add it _or_ the pybind11 specific directory
  # here.
  execute_process(
    COMMAND "${PYTHON_EXECUTABLE}" -c
            "import pybind11; print(pybind11.get_cmake_dir())"
    OUTPUT_VARIABLE _tmp_dir
    OUTPUT_STRIP_TRAILING_WHITESPACE COMMAND_ECHO STDOUT)
  cmake_print_variables(PYTHON_EXECUTABLE)
  cmake_print_variables(_tmp_dir)
  list(APPEND CMAKE_PREFIX_PATH "${_tmp_dir}")
# endif()

# Now we can find pybind11
find_package(pybind11 CONFIG REQUIRED)
find_package (Eigen3 REQUIRED)
find_package (Boost REQUIRED)


pybind11_add_module(_multiple_wave_transport MODULE 
  src/bindings.cpp 
  src/bind_wavepacket.cpp
  src/bind_integrator.cpp
  src/bind_three_wave_system.cpp
  src/wavepacket.cpp
  src/wavepacket.hpp
  src/type_definitions.hpp
  src/integrator.hpp
  src/integrator.cpp
  src/multiple_wave_system.hpp
  src/multiple_wave_system.cpp
  src/helper_collections.hpp
  src/helper_collections.cpp
  )


target_link_libraries(_multiple_wave_transport PUBLIC Eigen3::Eigen Boost::boost)

target_compile_definitions(_multiple_wave_transport PRIVATE VERSION_INFO=${PROJECT_VERSION})

target_compile_features(_multiple_wave_transport PUBLIC cxx_std_20)

set(COMPILE_OPTS 
        -Wall -Wextra -Wshadow -Wnon-virtual-dtor -pedantic
        -Wold-style-cast -Wcast-align -Wunused -Woverloaded-virtual
        -Wconversion -Wsign-conversion -Wmisleading-indentation
        -Wduplicated-cond -Wduplicated-branches -Wlogical-op
        -Wnull-dereference -Wuseless-cast -Wdouble-promotion
        -Wformat=2 -static-libstdc++
        -fPIC
        # -frounding-math
        $<$<CONFIG:Debug>:
        -g
        >
        $<$<CONFIG:Release>:
        -O3
        # -march=native
        >
        )


target_compile_options(_multiple_wave_transport PRIVATE ${COMPILE_OPTS})



install(TARGETS _multiple_wave_transport DESTINATION .)
