# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class Xfce4Terminal(AutotoolsPackage):
    """A lightweight and easy to use terminal emulator application for Xfce4"""

    homepage = "https://docs.xfce.org/apps/xfce4-terminal/start"
    url = "https://archive.xfce.org/src/apps/xfce4-terminal/1.1/xfce4-terminal-1.1.3.tar.bz2"
    list_url = "https://archive.xfce.org/src/apps/xfce4-terminal/"
    list_depth = 2

    def url_for_version(self, version):
        base = f"https://archive.xfce.org/src/apps/{self.name}"
        dirname = version.up_to(2)
        filename = f"{self.name}-{version}.tar.bz2"
        return join_path(base, dirname, filename)

    maintainers("teaguesterling")

    license("GPLv2", checked_by="teaguesterling")

    version("1.1.3", sha256="214dd588d441b69f816009682a3bb4652cc19bed7ea64b612a12f097417b3d45")
    version("1.1.2", sha256="79a85ee216502c7248e04d560adf8fef86b9d0e047f81e9ea4fe26fbda34d810")
    version("1.1.1", sha256="5ab5c9b49c00be29f0be4eee5ccfa5073b16f2456185270265a9324549080aa6")
    version("1.1.0", sha256="40823377242b9b09749f5d4a550f41d465153c235c31f34052f804d3453ad4a3")
    version("1.0.4", sha256="78e55957af7c6fc1f283e90be33988661593a4da98383da1b0b54fdf6554baf4")
    version("1.0.0", sha256="593b6a7bd9b18851e51854e075990109b7896a22713b5dd8b913b23f21db6576")

    depends_on("intltool@0.35:")

    depends_on("glib@2.44:")
    depends_on("gtkplus@3.22:")
    depends_on("pcre2@10.00:")
    depends_on("libxfce4ui@4.17:")
    depends_on("xfconf@4.16:")
    depends_on("libx11@1.6.7:")
    depends_on("vte@0.51.3:")

