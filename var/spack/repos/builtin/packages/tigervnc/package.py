# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
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
#     spack install tigervnc
#
# You can edit this file again by typing:
#
#     spack edit tigervnc
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack.package import *


class Tigervnc(CMakePackage):
    """A high-performance, platform-neutral implementation of VNC"""

    homepage = "https://tigervnc.org/"
    url = "https://github.com/TigerVNC/tigervnc/archive/refs/tags/v1.13.1.tar.gz"

    maintainers("teaguesterling")

    license("GNUv2", checked_by="teaguesterling")

    version("1.13.1", sha256="b7c5b8ed9e4e2c2f48c7b2c9f21927db345e542243b4be88e066b2daa3d1ae25")
    version("1.13.0", sha256="770e272f5fcd265a7c518f9a38b3bece1cf91e0f4e5e8d01f095b5e58c6f9c40")
    version("1.12.90", sha256="eac28ab565a66d33aeb766e80029a64846de92e3aa718e3b8f177096520be4c3")
    version("1.12.0", sha256="9ff3f3948f2a4e8cc06ee598ee4b1096beb62094c13e0b1462bff78587bed789")
    version("1.11.90", sha256="ee65c06612833984a7995dbeaa80af2fb966934e9069adfee47aa600fd88b543")
    version("1.11.0", sha256="3648eca472a92a4e8fe55b27cd397b1bf16bad0b24a3a1988661f44553f5e2c3")
    version("1.10.90", sha256="6bf85b9602194ac3518c234288c161236b83bd4c87a4e323c3000cdf556be844")
    version("1.10.1", sha256="19fcc80d7d35dd58115262e53cac87d8903180261d94c2a6b0c19224f50b58c4")
    version("1.10.0", sha256="a1e54d980eef8db06f5f696aa1fb6b98be049dac5205fda8b54f211a88dd182c")
    version("1.9.90", sha256="83fbcd48e7317f41a72329db4e9c2d37e109cfb11397ffc03ad16aab9b4b7f73")

    variant("pam", default=False, description="Build with PAM support")

    # https://github.com/TigerVNC/tigervnc/blob/master/BUILDING.txt

    with default_args(type=("build", "link", "run")):
        depends_on("zlib-api")
        depends_on("pixman")
        depends_on("fltk@1.3.3:")
        depends_on("gnutls")
        depends_on("libxrandr")
        depends_on("libxfixes")
        depends_on("gettext")
        depends_on("nettle")
        depends_on("libjpeg-turbo")

        depends_on("linux-pam", when="+pam")  # linux-pam doesn't build
        depends_on("libx11@1.6:")
        depends_on("ffmpeg")

    def cmake_args(self):
        args = []
        return args
