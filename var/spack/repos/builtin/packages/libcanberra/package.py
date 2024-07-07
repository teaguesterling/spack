# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libcanberra(AutotoolsPackage):
    """libcanberra is an implementation of the XDG Sound Theme and
    Name Specifications, for generating event sounds on free desktops,
    such as GNOME."""

    homepage = "https://0pointer.de/lennart/projects/libcanberra/"
    url = "https://0pointer.de/lennart/projects/libcanberra/libcanberra-0.30.tar.xz"

    license("LGPL-2.1-or-later")

    version("0.30", sha256="c2b671e67e0c288a69fc33dc1b6f1b534d07882c2aceed37004bf48c601afa72")

    # TODO: Add variants and dependencies for the following audio support:
    # ALSA, OSS, PulseAudio, udev, GStreamer, null, GTK3+ , tdb

    variant("oss", default=False, description="Enable OSS support")
    variant("alsa", default=True, description="Enable ALSA support")
    variant("gtk", default=False, description="Enable optional GTK+ support")
    variant("gtk3", default=False, description="Enable optional GTK+ 3 support")
    variant("pulse", default=False, description="Enable optional pulseaudio support")
    variant("udev", default=False, description="Enable optional udev support")

    with default_args(type=("build", "link", "run")):
        depends_on("libvorbis")
        depends_on("alsa-lib", when="+alsa")
        with when("+gtk3"):
            depends_on("gtkplus")
            depends_on("gtkplus@3", when="+gtk3")
            depends_on("libxrender")
            depends_on("libxext")
            depends_on("libx11")
            depends_on("libxinerama")
            depends_on("libxrandr")
            depends_on("libxcursor")
            depends_on("libxcomposite")
            depends_on("libxdamage")
            depends_on("libxfixes")
            depends_on("libxcb")
            depends_on("libxau")

        depends_on("pulseaudio", when="+pulse")
        depends_on("systemd", when="udev")

    with default_args(type=("build", "link")):
        depends_on("libtool")
        depends_on("pkgconfig")

    def configure_args(self):
        args = ["--enable-static"]

        args += self.enable_or_disable("oss")
        args += self.enable_or_disable("alsa")
        args += self.enable_or_disable("gtk")
        args += self.enable_or_disable("gtk3")
        args += self.enable_or_disable("pulse")
        args += self.enable_or_disable("udev")

        return args
