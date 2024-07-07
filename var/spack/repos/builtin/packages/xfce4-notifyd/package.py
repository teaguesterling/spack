# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class Xfce4Notifyd(AutotoolsPackage):
    """a notification service for the Xfce Desktop."""

    homepage = "https://docs.xfce.org/apps/xfce4-notifyd/start"
    url = "https://archive.xfce.org/src/apps/xfce4-notifyd/0.9/xfce4-notifyd-0.9.4.tar.bz2"

    maintainers("teaguesterling")

    license("GPLv2", checked_by="teaguesterling")

    version("0.9.4", sha256="ae6c128c055c44bd07202f73ae69ad833c5e4754f3530696965136e4d9ea7818")
    version("0.9.3", sha256="79ee4701e2f8715a700de2431aa33682933cab18d76938bb18e2820302bbe030")
    version("0.9.2", sha256="47590f0c1f5cb45652d63e17cb4202bee2b2136432ac42395a4bedd110d18789")
    version("0.9.1", sha256="ecbe017515b6c5c3b2f2882451d351a0b6735d80313039c6dde207dd96534fea")
    version("0.9.0", sha256="be4a6e9b8fb28a6fc1321783cb48a5b7f16a4ca9f89cd905f11f32e4f2eadabc")

    depends_on("glib@2.68:")
    depends_on("gtkplus@3.22:")
    depends_on("libxfce4util@4.12.0:")
    depends_on("libxfce4ui@4.12.0:")
    depends_on("xfconf@4.10:")
    depends_on("libnotify@0.7:")
    depends_on("xfce4-panel@4.10.0:")
    depends_on("sqlite@3.34:")
    depends_on("libcanberra@0.30:")
    depends_on("libtool")
