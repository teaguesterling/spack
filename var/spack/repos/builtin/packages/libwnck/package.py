# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class Libwnck(MesonPackage, AutotoolsPackage):
    """Window Navigator Construction Kit"""

    homepage = "https://gitlab.gnome.org/GNOME/libwnck"
    url = "https://download.gnome.org/sources/libwnck/3.4/libwnck-3.4.9.tar.xz"
    list_url = "https://download.gnome.org/sources/libwnck/"
    list_depth = 2

    def url_for_version(self, version):
        base = "https://download.gnome.org/sources/libwnck"
        dirname = version.up_to(1) if version >= Version("40") else version.up_to(2)
        filename = f"libwnck-{version.up_to(3)}.tar.xz"
        return f"{base}/{dirname}/{filename}"

    license("GPLv2", checked_by="teaguesterling")

    version("43.0", sha256="905bcdb85847d6b8f8861e56b30cd6dc61eae67ecef4cd994a9f925a26a2c1fe")
    version("40.1", sha256="03134fa114ef3fbe34075aa83678f58aa2debe9fcef4ea23c0779e28601d6611")
    version("3.36.0", sha256="bc508150b3ed5d22354b0e6774ad4eee465381ebc0ace45eb0e2d3a4186c925f")
    version("3.31.4", sha256="45b3f64bb881bab5666d93bc8ad7fef96c2820b0a3dfd117026b0d121767dd26")
    version("3.24.1", sha256="afa6dc283582ffec15c3374790bcbcb5fb422bd38356d72deeef35bf7f9a1f04")
    version("3.20.1", sha256="1cb03716bc477058dfdf3ebfa4f534de3b13b1aa067fcd064d0b7813291cba72")
    version("3.14.1", sha256="bb643c9c423c8aa79c59973ce27ce91d3b180d1e9907902278fb79391f52befa")
    version("3.4.9", sha256="96e6353f2701a1ea565ece54d791a7bebef1832d96126f7377c54bb3516682c4")

    variant("introspection", default=True, description="Build with gobject-introspection support")
    variant("notification", default=True, description="Build with startup-notification support")
    variant("tools", default=True, description="Install WNCK tools")

    build_system(
        conditional("meson", when="@3.31:"),
        conditional("autotools", when="@:3.24"),
        default="meson",
    )

    depends_on("intltool@0.40.6:", type="build")
    with default_args(type=("build", "link", "run")):
        depends_on("gobject-introspection", when="+introspection")
        depends_on("startup-notification", when="+notification")

        depends_on("glib@2")
        depends_on("gdk-pixbuf")
        depends_on("gtkplus@3.22:")

    def configure_args(self):
        args = []

        args += self.enable_or_disable("introspection")
        args += self.enable_or_disable("tools")
        args += self.enable_or_disable("notification")

        return args
