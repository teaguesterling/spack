# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.build_systems.bundle import PureBundlePackage
from spack.package import *


class SpackosBase(PureBundlePackage):
    homepage = "https://github.com/spack/spack"
    # NOTE: this refers to glibc's 2.38 tarball to shut up the URL fetcher
    version("0.2.0")

    with when("os=spackos"):
        depends_on("glibc+spack-os-stage=2")
        depends_on("libxcrypt+spack-os-stage=2")

    @property
    def os_info(self):
        return {
            "NAME": "SpackOS",
            "VERSION": f"{self.spec.version.up_to(2)} (Take 2)",
            "ID": "spackos",
            "VERSION_ID": f"{self.spec.version}",
            "PRETTY_NAME": f"SpackOS {self.spec.version.up_to(1)} (Take 2)",
            "HOME_URL": "https://spack.io",
            "SUPPORT_URL": "https://github.com/spack/spack/issues",
            "PRIVACY_POLICY_URL": "https://spack.io/about/",
        }

    def write_os_release_file(self, info):
        mkdirp(prefix.usr.lib)
        rel_path = "usr/lib/os-release"
        with open(prefix.usr.lib.join("os-release"), "wt") as f:
            for k, v in info.items():
                print(f"{k}={v!r}", file=f)
        symlink(join_path("..", rel_path), prefix.etc.join("os-release"))

    def install(self, spec, prefix):
        self.write_os_release_file(self.os.info)
