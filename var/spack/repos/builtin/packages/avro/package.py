# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import inspect
import os
import contextlib

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

    @property
    def variant_sub_builders(self):
        return [
            ("+c", CMakeBuilder, {"build_directory": "build/c", "root_cmakelists_dir": "lang/c"}),
            ("+cxx", CMakeBuilder, {"build_directory": "build/c++", "root_cmakelists_dir": "lang/c++"}),
        ]


class BuilderOverrider:
    # This is a hack to allow us to build multiple targets in the same 
    # package based on variants
    @contextlib.contextmanager
    def with_sub_builder_overrides(self, **kwargs):
        old = {}
        for key, new_value in kwargs.items():
            old[key] = getattr(self, key)
            setattr(self, key, new_value)
        yield
        for key, old_value in kwargs.items():
            setattr(self, key, old_value)

    def create_wrapped_method(self, method, variant, required_builder, overrides):
        current_builder == type(self)
        fn = getattr(self, method)
        def wrapped(*args, **kwargs):
            if required_builder == current_builder and self.spec.satisfies(variant):
                with self.sub_builder_overrides(**overrides):
                    return fn(*args, **kwargs)


class CMakeBuilder(spack.build_systems.cmake.CMakeBuilder, BuilderOverrider):
    def cmake(self, pkg, spec, prefix):
        for sub_builder_def in pkg.variant_sub_builders():
            cmake = self.wrapped_method("cmake", *sub_builder_def)
            cmake(pkg, spec, prefix)

    def build(self, pkg, spec, prefix):
        for sub_builder_def in pkg.variant_sub_builders():
            build = self.wrapped_method("build", *sub_builder_def)
            build(pkg, spec, prefix)

    def install(self, pkg, spec, prefix):
        for sub_builder_def in pkg.variant_sub_builders():
            install = self.wrapped_method("install", *sub_builder_def)
            install(pkg, spec, prefix)
