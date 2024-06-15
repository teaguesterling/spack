# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class Vte(MesonPackage):
    """A virtual terminal widget for GTK applications."""

    homepage = "https://gitlab.gnome.org/GNOME/vte"
    url = "https://gitlab.gnome.org/GNOME/vte/-/archive/0.76.3/vte-0.76.3.tar.gz"
    list_url = "https://gitlab.gnome.org/GNOME/vte/-/archive/"
    list_depth = 2

    license("CC-BY-4-0", checked_by="teaguesterling")

    version("0.76.3", sha256="eb6d80b879914b89c22811743a5d779fa0e9c57acfa925873b521d054b809746")

    variant("icu", default=True, description="Build with icu4u support")
    variant("gnutls", default=True, description="Build with gnutls support")
    variant("vala", default=True, description="Build with Vala support")
    variant("introspection", default=True, description="Build with gobject introspection support")
    variant("systemd", default=False, description="Build with systemd support")

    depends_on("meson@0.60:", type="build")
    depends_on("cmake")

    depends_on("gtkplus@3.24:")
    depends_on("pcre2@10.21:")
    depends_on("libxml2@2:")

    depends_on("icu4c", when="+icu")
    depends_on("gnutls@3.2.7:", when="+gnutls")
    depends_on("vala@0.56.17:", when="+vala")
    depends_on("glib@2.72:", when="+introspection")
    depends_on("gobject-introspection", when="+introspection")
    depends_on("systemd", when="+systemd")

    depends_on("cairo@1:")
    depends_on("lz4@1.9")

    def true_or_false(self, arg, activation_value="true", variant=None):
        deactivation_value = "false"
        variant = f"+{arg}" if variant is None else variant
        active = self.spec.satisfies(variant)
        value = activation_value if active else deactivation_value
        return [
            f"-D{arg}={value}"
        ]

    def meson_args(self):

        args = [
            "-Dgtk3=true",   # We can only build with GTK3
            "-Dgtk4=false",  # We can't build with GTK4 support
        ]

        args += self.true_or_false("icu")
        args += self.true_or_false("gnutls")
        args += self.true_or_false("vapi", variant="+vala")
        args += self.true_or_false("gir", variant="+introspection")
        args += self.true_or_false("_systemd", variant="+systemd")

        return args

