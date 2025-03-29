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

    # See: https://github.com/ctypesgen/ctypesgen/issues/181
    # This fixes syntax errors when parsing /usr/include/sys/cdefs.h
    patch(
        "https://patch-diff.githubusercontent.com/raw/ctypesgen/ctypesgen/pull/207.patch", 
        sha256="eacd9144f0e99df1dfdc43a3e504fc399e997f1270d56dcfc013b98529f518ce",
        when="@:1.1.1",
    )

    depends_on("c", type="build")

    depends_on("py-setuptools@64:", type="build")
    depends_on("py-setuptools-scm@7.1", type="build")
