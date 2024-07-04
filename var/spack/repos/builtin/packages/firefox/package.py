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
#     spack install firefox
#
# You can edit this file again by typing:
#
#     spack edit firefox
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack.package import *
from spack.util.prefix import Prefix
from textwrap import dedent




class Firefox(Package):
    """The FireFox web browser by Mozilla"""

    homepage = "https://www.firefox.com"
    url = "https://archive.mozilla.org/pub/firefox/releases/127.0/source/firefox-127.0.source.tar.xz"

    maintainers("teaguesterling")

    license("MPL", checked_by="teaguesterling")

    version("127.0", sha256="ea6b089ff046ca503978fdaf11ea123c64f66bbcdc4a968bed8f7c93e9994321")

    phases = ["configure", "build", "install"]

    # From Arch build notes
    depends_on("dbus-glib")
    depends_on("ffmpeg")
    depends_on("gtkplus@3")
    depends_on("libxscrnsaver")
    depends_on("libxt")
    depends_on("nss")
    depends_on("pulseaudio")
    depends_on("shared-mime-info")

    # Needed for mach build/configure
    depends_on("libx11")
    depends_on("libxcb")
    depends_on("libxext")
    depends_on("libxrandr@1.4.0:")
    depends_on("libxcursor")
    depends_on("libxdamage")
    depends_on("libxcomposite")
    depends_on("libxkbcommon")

    with default_args(type="build"):
        depends_on("binutils")
        depends_on("diffutils")
        depends_on("git")
        depends_on("imake")
        depends_on("llvm")
        depends_on("mesa")
        depends_on("nasm")
        depends_on("node-js")
        depends_on("pciutils")
        depends_on("pkgconfig")
        depends_on("python@3.6:3.11")
        depends_on("rust")
        depends_on("unzip")
        depends_on("wasi-sdk@14:")
        depends_on("wget")
        depends_on("yasm")
        depends_on("zip")

        depends_on("cbindgen")
        depends_on("generate-ninja")

        with when("@127.0"):
            depends_on("py-semver@2.13.0:")
            depends_on("py-appdirs@1.4:")
            depends_on("py-click@7:")
            depends_on("py-diskcache@4:")
            depends_on("py-jinja2@2.10.1:")
            depends_on("py-jsonschema@3.0.2:")
            depends_on("py-pyyaml@5.3.1:")
            depends_on("py-markupsafe@2.0:")
            depends_on("py-pyrsistent@0.15.0:")  # This states 0.14.0 but we need it a bit higher
            depends_on("py-six")

            # These are strictly limited or bounded in the pyproject.toml
            depends_on("py-psutil@5.4.2:5.9.4")
            depends_on("py-zstandard@0.11.1:0.22.0")
            depends_on("py-attrs@17.4.0")
            depends_on("py-glean-sdk@60.0.1")
            depends_on("py-glean-parser@14.0")

    # Noted in mach requirements
    conflicts("py-pyrsistent@0.17.0:0.17.2")

    def mach(self, command, *args):
        mach = which("./mach")
        print(f"Running {mach} {command} {args}")
        return mach("--verbose", command, *args)

    @property
    def build_cache_dir(self):
        return Prefix(f"{self.stage.source_path}/.mozbuild")

    @property
    def build_config(self):
        return self.build_cache_dir.join("mozconfig-firefox")

    def setup_build_enviroment(self, env):
        env.set("MOZBUILD_STATE_PATH", self.build_cache_dir)
        env.set("MOZCONFIG", self.build_config)
        env.set("GN", self.spec["generate-ninja"].home.bin.gn)
        env.set("RUSTC_OPT_LEVEL", "2")

    def patch(self):
        # Make the wasi clib available without re-downloading
        mozbuild = self.build_cache_dir
        mkdirp(mozbuild.wrlb)
        symlink(self.spec["wasi-sdk"].home, mozbuild.wrlb.join("wasi-sysroot"))

    def build_args(self):
        args = []
        args.append(f"--jobs={make_jobs}")
        return args

    def configure_args(self):
        args = []
        args += [
            "--without-wasm-sandboxed-libraries",  # Required to use wasi-sdk
            "--enable-application=browser",        # Build the desktop browser (not android)
            "--enable-release",
            "--enable-lto=full",
            "MOZ_PGO=1",
        ]
        return args

    def configure(self, spec, prefix):
        self.mach("configure", *self.configure_args())

    def build(self, spec, prefix):
        self.mach("build", *self.build_args())

    def install(self, spec, prefix):
        # install
        pass




