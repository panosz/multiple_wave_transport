import sys

try:
    from skbuild import setup
    from skbuild import cmaker
except ImportError:
    print(
        "Please update pip, you need pip 10 or greater,\n"
        " or you need to install the PEP 518 requirements in pyproject.toml yourself",
        file=sys.stderr,
    )
    raise

from setuptools import find_packages

setup(
    name="multiple_wave_transport",
    version="0.0.1",
    description="1D transport from multiple electrostatic waves",
    author="Panagiotis Zestanakis",
    license="MIT",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    cmake_install_dir="src/multiple_wave_transport",
    include_package_data=True,
    extras_require={"test": ["pytest"]},
    python_requires=">=3.10",
    cmake_with_sdist=True,
)
