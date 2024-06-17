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
#     spack install xfce4-taskmanager
#
# You can edit this file again by typing:
#
#     spack edit xfce4-taskmanager
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack.package import *


class Xfce4Taskmanager(AutotoolsPackage):
    """Easy to use task manager for Xfce4"""

    homepage = "https://docs.xfce.org/apps/xfce4-taskmanager/start"
    url = "https://archive.xfce.org/src/apps/xfce4-taskmanager/1.5/xfce4-taskmanager-1.5.7.tar.bz2"

    maintainers("teaguesterling")

    license("GPLv2", checked_by="teaguesterling")

    version("1.5.7", sha256="6736832f5a64533e536f4994280bd907da19666cda8d2f465c8a53bb581f68bb")
    version("1.5.6", sha256="20979000761a41faed4f7f63f27bd18bb36fb27db4f7ecc8784a460701fb4abb")
    version("1.5.5", sha256="f64f01ba241a0b8bbf2ed3274e5decc2313c9f8b0e4d160db3ba69b331558ae5")
    version("1.5.4", sha256="25b13e890d14ce453ece19eb6201b4a9a4f3e3b324b947db9047ce79cc3ae62a")
    version("1.5.3", sha256="bd18323705ea677f1c0f3de4dde1a3bf2ee50956ae5c47c177c0c98daab1428a")
    version("1.5.2", sha256="bd25143f47a29000b4148874863dffa521b1a37cb01dbc026f423ea3160f9a35")
    version("1.5.1", sha256="cde3ff05710f4661acd3d7a5a66ad2daee8c0498a31c115e49c778463a1dd55e")
    version("1.5.0", sha256="089b9f1064e412fbc11a821e4087015f6f46b7ae0833fc81a581164769bb4f1b")

    variant("x11", default=True, description="Build with X11 support")
    variant("icons", default=True, description="Build with icon support")

    depends_on("intltool", type="build")

    depends_on("glib@2.50.0:")
    depends_on("gtkplus@3.22.0:")
    depends_on("libxmu@1.1.2:")
    depends_on("cairo@1.5.0:")
    depends_on("libxfce4ui@4.14.0:")
    depends_on("xfconf@4.14.0:")
    depends_on("libx11@1.6.7:", when="+x11")
    depends_on("libwnck@3.2:", when="+icons")

