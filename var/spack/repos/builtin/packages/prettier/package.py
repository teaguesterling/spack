# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *
from spack.build_systems.npm import NpmPackage


class Prettier(NpmPackage):
    """Prettier is an opinionated code formatter."""

    homepage = "https://prettier.io/"
    url = "https://registry.npmjs.org/prettier/-/prettier-3.5.3.tgz"
    git = "https://github.com/prettier/prettier.git"

    maintainers("adamjstewart", "teaguesterling")
    license("MIT")

    version("3.5.3", sha256="14841de7b71a93123d22997db22d088debb13976778d869e3622199108e85b4b")
    version("3.2.5", sha256="0ac58fbe50859feb06099670526460cef7f51c83fee458b02fc67e53ffd23f57")
    version("3.0.0", sha256="12dacd9a4190815daa0acd7f45ca69f0c39d152b1c4a7f6c6ae2de38ccb0e20c")
    version("2.8.8", sha256="30d7f0b35843102c2aec6033751bd2a789fafde6ad1c22a93b6ab6d3d6b3cb0c")
    version("2.0.0", sha256="20770b3c1d6db6a9c6bcbd1d13465a588d5e6e28087f22d1bc6c22f095e75cd2")
