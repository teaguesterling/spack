# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class Ristretto(AutotoolsPackage):
    """Ristretto image viewer for Xfce4"""

    homepage = "https://docs.xfce.org/apps/ristretto/start"
    url = "https://archive.xfce.org/src/apps/ristretto/0.13/ristretto-0.13.2.tar.bz2"

    maintainers("teaguesterling")

    license("GPLv2", checked_by="teaguesterling")

    version("0.13.2", sha256="779f5ede3016019eec01d64a025583078d3936e35d4288ec2e8433494d757dd9")
    version("0.13.1", sha256="d71affbf15245067124725b153c908a53208c4ca1ba2d4df1ec5a1308d53791e")
    version("0.13.0", sha256="596676b41daada390c8d83e5bb83be6832a260f4bf0dbcc651ac0b68c0f4e301")

    depends_on("glib@2.56:")
    depends_on("gtkplus@3.22:")
    depends_on("libxfce4util@4.16:")
    depends_on("libxfce4ui@4.16:")
    depends_on("xfconf@4.12.1:")
    depends_on("libexif@0.6.0:")
    depends_on("cairo@1.10:")
    depends_on("libx11@1.6.7:")

