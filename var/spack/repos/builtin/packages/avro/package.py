# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import inspect
import os

from llnl.util import filesystem as fs

import spack.build_systems.cmake
from spack.package import *


class Avro(Package):
    """Apache Avro data serialization system."""

    homepage = "https://www.apache.org/dyn/closer.cgi/avro/"
    url = "https://github.com/apache/avro/archive/refs/tags/release-1.12.0.tar.gz"

    maintainers("teaguesterling")

    license("Apache-2.0", checked_by="teaguesterling")

    version("1.12.0", sha256="08bd6a53766246b66d9c8cd167a8fad227c2c8581ca2f3586bf1d9538f3e8f7b")
    version("1.11.3", sha256="6ea787a83260a11b5a899aadd22f701e24138477cd7bf789614051a449dcc034")

    list_url = "https://downloads.apache.org/avro/"
    list_depth = 1

    variant("c", default=True, description="Built the C library")
    variant("cxx", default=True, description="Built the C++ library")
    variant("rust", default=False, description="Build the Rust library")
    # TODO: java, javascript, perl, python, ruby, rust

    # Had issues with linking in C lib on my build
    variant("snappy", default=True, description="Build with snappy support")
    variant("zlib", default=True, description="Build with zlib support")

    with default_args(type=("build")):
        depends_on("pkgconfig")
        depends_on("python@3")
        depends_on("doxygen")

    depends_on("snappy+shared", when="+snappy")
    depends_on("zlib-api")

    with when("+c"):
        depends_on("c", type="build")
        depends_on("asciidoc", type="build")
        depends_on("cmake@2.6:")
        depends_on("jansson@2.3:", type=("build", "link"))

    with when("+cxx"):
        depends_on("cxx", type="build")
        depends_on(
            "boost@1.38:+iostreams+filesystem+system+program_options+regex visibility=global",
            type=("build", "link"),
        )
        depends_on("cmake@2.6:")

    with when("+rust"):
        depends_on("cargo", type="build")

    def cmake_variant_subdirs(self):
        return [
            ("build/c", "lang/c", [], "+c"), 
            ("build/c++", "lang/c++", [], "+cxx"),
        ]


class CMakeBuilder(spack.build_systems.cmake.CMakeBuilder):
    def cmake_subdir(self, pkg, spec, prefix, builddir, listdir, cmake_args, variant):
        """Runs ``cmake`` in the build sub directory if variant is true"""
        if spec.satisfies(variant):
            options = self.std_cmake_args
            options += self.cmake_args()
            options += cmake_args
            options.append(os.path.abspath(listdir))
            with fs.working_dir(builddir, create=True):
                inspect.getmodule(self.pkg).cmake(*options)

    def build_subdir(self, pkg, spec, prefix, builddir, variant):
        """Make the build sub targets"""
        if spec.satisfies(variant):
            with fs.working_dir(builddir):
                if self.generator == "Unix Makefiles":
                    inspect.getmodule(self.pkg).make(*self.build_targets)
                elif self.generator == "Ninja":
                    self.build_targets.append("-v")
                    inspect.getmodule(self.pkg).ninja(*self.build_targets)

    def install_subdir(self, pkg, spec, prefix, builddir, variant):
        """Make the install sub targets"""
        if spec.satisfies(variant):
            with fs.working_dir(builddir):
                if self.generator == "Unix Makefiles":
                    inspect.getmodule(self.pkg).make(*self.install_targets)
                elif self.generator == "Ninja":
                    inspect.getmodule(self.pkg).ninja(*self.install_targets)

    def cmake(self, pkg, spec, prefix):
        for builddir, listdir, cmake_args, variant in pkg.cmake_variant_subdirs():
            self.cmake_subdir(pkg, spec, prefix, builddir, listdir, cmake_args, variant)

    def build(self, pkg, spec, prefix):
        for builddir, listdir, cmake_args, variant in pkg.cmake_variant_subdirs():
            self.build_subdir(pkg, spec, prefix, builddir, variant)

    def install(self, pkg, spec, prefix):
        for builddir, listdir, cmake_args, variant in pkg.cmake_variant_subdirs():
            self.install_subdir(pkg, spec, prefix, builddir, variant)
