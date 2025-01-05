# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import inspect
import sys

from llnl.util import filesystem as fs

import spack.builder
from spack.build_systems.cmake import CMakeBuilder
from spack.build_systems.cargo import CargoBuilder
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
    
    # TODO: java, javascript, perl, python, ruby, rust
    variant(
        "language",
        default="c,cxx",
        values=("c", "cxx", "rust"),
        multi=True,
        description="Language bindings to build",
    )
    variant("ninja_generator", default=False, description="Use Ninja in CMake builds")

    # Had issues with linking in C lib on my build
    variant("snappy", default=True, description="Build with snappy support")
    variant("zlib", default=True, description="Build with zlib support")

    with default_args(type=("build")):
        depends_on("pkgconfig")
        depends_on("python@3")
        depends_on("doxygen")

    depends_on("snappy+shared", when="+snappy")
    depends_on("zlib-api")

    with when("language=c,cxx"):
        depends_on("cmake@2.6:", type="build")
        depends_on("gmake", type="build", when="~ninja_generator")
        depends_on("ninja", type="build", when="+ninja_generator")

    with when("language=c"):
        depends_on("c", type="build")
        depends_on("asciidoc", type="build")
        depends_on("jansson@2.3:", type=("build", "link"))

    with when("language=cxx"):
        depends_on("cxx", type="build")
        depends_on(
            "boost@1.38:+iostreams+filesystem+system+program_options+regex visibility=global",
            type=("build", "link"),
        )

    with when("language=rust"):
        depends_on("rust", type="build")

    @property
    def phases(self):
        phases = ["setup_package"]
        for builder in self.sub_builders():
            for phase in builder.phases:
                if phase not in phases:
                    phases.append(phase)
        return phases


    def build_when(self, variant, builder):
        if self.spec.satisfies(variant):
            return [builder]
        else:
            return []
   
    def sub_builders(self):
        builders = []
        builders += self.build_when("language=c", AvroCCMakeBuilder(self))
        builders += self.build_when("language=cxx", AvroCXXCMakeBuilder(self))
        builders += self.build_when("language=rust", AvroCargoBuilder(self))
        return builders
    
    def get_phase_runner(self, name):
        sub_phases = []
        for builder in self.sub_builders():
            if name in builder.phases:
                sub_phases.append(getattr(builder, name))

        def runner(*args):
            for sub_phase in sub_phases:
                sub_phase(self, *args)

        return runner

    def run_phase(self, name, *args):
        self.get_phase_runner(name)(*args)

    def setup_package(self, spec, prefix):
        # Hack
        for builder in self.sub_builders():
            if hasattr(builder, "setup_package"):
                builder.setup_package(self.module, spec)

    def __getattr__(self, item):
        if item in self.phases:
            print(" GETTING PHASE", item)
            return self.get_phase_runner(item)
        else:
            return super().__getattr__(item)


class AvroSubBuilder(spack.builder.Builder):
    sub_package = ...
    create_build_dir = True

    @property
    def parent_build_directory(self):
        return super().build_directory

    @property
    def build_directory(self):
        build_dir = join_path(self.parent_build_directory, "build", self.sub_package)
        if self.create_build_dir:
            makedirs(build_dir, exist_ok=True)
        return build_dir

    @property
    def sub_package_source(self):
        return join_path(self.pkg.stage.source_path, "lang", self.sub_package)


class AvroCMakeBuilder(AvroSubBuilder, CMakeBuilder):
    phases = ["cmake", "build", "install"]

    def setup_package(self, package, spec):
        setattr(package, "cmake", which("cmake"))
        if spec.satisfies("+ninja_generator"):
            setattr(package, "ninja", which("ninja"))
        else:
            setattr(package, "make", which("make"))

    @property
    def generator(self):
        if self.pkg.spec.satisfies("+ninja_generator"):
            return "Ninja"
        else:
            return "Unix Makefiles"

    @property
    def root_cmakelists_dir(self):
        return self.sub_package_source


class AvroCCMakeBuilder(AvroCMakeBuilder):
    sub_package = "c"


class AvroCXXCMakeBuilder(AvroCMakeBuilder):
    sub_package = "c++"


class AvroCargoBuilder(AvroSubBuilder, CargoBuilder):
    sub_package = "rust"

    def build(self, pkg, spec, prefix):
        with fs.working_dir(join_path(self.sub_package_source, "avro")):
            pkg.module.cargo(
                "build",
                "--all-features",
                "--release",
                "--lib",
                "--workspace",
                "--target-dir",
                join_path(self.build_directory, "out"),
                *self.build_args,
            )
    
#    def install(self, pkg, spec, prefix):
#        target = prefix.lib.avro.rust
#        makedirs(target)


