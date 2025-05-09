# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import re

from spack.package import *
from spack.build_systems.npm import NpmPackage


class Typescript(NpmPackage):
    """TypeScript is a superset of JavaScript that compiles to clean JavaScript output."""
    
    # Control whether to run the build script
    has_build_script = False

    homepage = "https://www.typescriptlang.org"
    url = "https://registry.npmjs.org/typescript/-/typescript-5.3.2.tgz"
    git = "https://github.com/microsoft/TypeScript.git"

    tags = ["build-tools"]

    license("Apache-2.0")

    version("5.3.2", sha256="62d487dcc3e0f4cfaa3b752f282807e6cb34e5f9d4ea82cd8aa5071e713c21f1")

    executables = ["^tsc$"]

    @classmethod
    def determine_version(cls, exe):
        output = Executable(exe)("--version", output=str, error=str)
        match = re.match(r"Version\s+([\d.]+)\s*", output)
        return match.group(1) if match else None
