# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class Vte(MesonPackage):
    """A virtual terminal widget for GTK applications."""

    homepage = "https://gitlab.gnome.org/GNOME/vte"
    url = "https://gitlab.gnome.org/GNOME/vte/-/archive/0.76.3/vte-0.76.3.tar.gz"
    list_url = "https://gitlab.gnome.org/GNOME/vte/-/tags"
    list_depth = 1

    license("CC-BY-4-0", checked_by="teaguesterling")

    version("0.76.3", sha256="eb6d80b879914b89c22811743a5d779fa0e9c57acfa925873b521d054b809746")
    version("0.75.92", sha256="c334eb26b6c67da8c2990eebe3c498520dad949522ba21df48295aff99285f14")
    version("0.74.2", sha256="03a5a41c777d233341753d8ecd23c882e76f6464310bb2b8065425a1c859060a")
    version("0.73.99", sha256="a4dedc1c8f3f62a3bff5c5da1dc2458f3f8cc30e884426f512f932aa37361e94")
    version("0.72.4", sha256="aaee5620d654c83a3298bce89852259188fdc79c15c121aa5d316cf5a2500b3f")
    version("0.70.6", sha256="caf4bfc8f02b633bc16658559ced98101e82da4efb80b72ff3ef7d98325e2aa8")

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

    conficts("%gcc@:9", when="@0.76:")

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

