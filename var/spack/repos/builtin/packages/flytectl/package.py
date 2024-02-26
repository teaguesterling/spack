# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install flytectl
#
# You can edit this file again by typing:
#
#     spack edit flytectl
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack.package import *


class Flytectl(MakefilePackage):
    """ A cross platform CLI for Flyte. Written in Golang. Offers an intuitive interface to Flyte."""

    homepage = "https://docs.flyte.org/projects/flytectl/en/latest/"
    url = "https://github.com/flyteorg/flytectl/"

    maintainers("teaguesterling")

    license("apache")

    version("0.8.13", sha256="2119a1be42fde70fca0de8ff36f951034b475690de86fc336acd8a976cc7edeb")
    version("0.8.12", sha256="963b89ca67780d510719d139ee3b2357f564fc9c25ef3300b12c63fa312b72f3")
    version("0.8.11", sha256="9405bc32806744d774b6c9db23270a08a9528e29c5e0fc8819c76dbb90a5144c")
    version("0.8.10", sha256="f9cc9ba806c5e7b44cabde84979d45a2ce6adff98b10fc005048d8d30b3eee56")
    version("0.8.9", sha256="3e042fcb1e2bb0782adfeef1eeb7dfabbd00b80ff8aa8b44fc8b199074c45c63")

    def url_for_version(self, version):
        return "{0}/archive/refs/tags/v{1}.tar.gz".format(self.url, version)

    depends_on("go")

    build_targets = ["compile"]

    def install(self, spec, prefix):
        mkdir(prefix.bin)
        install("bin/flytectl", prefix.bin)

        # HACK to cleanup go modules with the user write bit unset
        import os, stat
        all_usr = stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR
        for root, dirs, files in os.walk(prefix.pkg):
            for child in dirs + files:
                os.chmod(os.path.join(root, child), all_usr)

