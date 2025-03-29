# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyCtypesgen(PythonPackage):
    """Pure-python wrapper generator for ctypes"""

    homepage = "https://github.com/ctypesgen/ctypesgen"
    pypi = "ctypesgen/ctypesgen-1.1.1.tar.gz"

    license("BSD", checked_by="teaguesterling")

    version("1.1.1", sha256="deaa2d64a95d90196a2e8a689cf9b952be6f3366f81e835245354bf9dbac92f6")

    depends_on("c", type="build")

    depends_on("py-setuptools@64:", type="build")
    depends_on("py-setuptools-scm@7.1", type="build")
