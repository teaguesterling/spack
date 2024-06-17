# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class Mousepad(AutotoolsPackage):
    """A simple text editor for Xfce4"""

    homepage = "https://docs.xfce.org/apps/mousepad/start"
    url = "https://archive.xfce.org/src/apps/mousepad/0.6/mousepad-0.6.2.tar.bz2"
    list_url = "https://archive.xfce.org/src/apps/mousepad/"
    list_depth = 2

    maintainers("teaguesterling")

    license("GPLv2", checked_by="teaguesterling")

    version("0.6.2", sha256="e7cacb3b8cb1cd689e6341484691069e73032810ca51fc747536fc36eb18d19d")
    version("0.6.1", sha256="560c5436c7bc7de33fbf3e9f6cc545280772ad898dfb73257d86533880ffff36")
    version("0.6.0", sha256="2253a5c582b8a899d842a8e4311d6b760435ad7cca493ff4edf305b89c1913d4")

    variant("plugin-shortcuts", default=True, description="Build the shortcuts plugin")
    #variant("plugin-gspell", default=False, description="Build the gspell plugin")

    depends_on("glib@2.52:")
    depends_on("gtkplus@3.24:")
    depends_on("gtksourceview@3.24:,4:")
    depends_on("libxfce4ui@4.17.5:", when="+plugin-shortcuts")
#    depends_on("libgspell@1.6.0:", when="+plugin-gspell")

    def flag_handler(self, name, flags):
        if name == "cflags":
            # Fails to check in xcfe4 include for the libxfce4kbd-private-3 tree
            flags.append(f"-I{self.spec['libxfce4ui'].home.include.xfce4}")
        return (flags, None, None)


