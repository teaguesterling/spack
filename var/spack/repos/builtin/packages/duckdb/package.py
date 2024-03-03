# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Duckdb(MakefilePackage):
    """DuckDB is an in-process SQL OLAP Database Management System."""

    homepage = "https://duckdb.org"
    url = "https://github.com/duckdb/duckdb/archive/refs/tags/v0.9.2.tar.gz"
    git = "https://github.com/duckdb/duckdb.git"

    license("MIT")
    maintainers("glentner")
    maintainers("teaguesterling")

    version("master", branch="master")
    version("0.10.0", sha256="5a925b8607d00a97c1a3ffe6df05c0a62a4df063abd022ada82ac1e917792013")
    version("0.9.2", sha256="afff7bd925a98dc2af4039b8ab2159b0705cbf5e0ee05d97f7bb8dce5f880dc2")
    version("0.9.1", sha256="37a43188d9354ce3ca101b2b118d867f5f76d04c3b83c09d86fd7508351a631b")
    version("0.9.0", sha256="3dbf3326a831bf0797591572440e81a3d6d668f8e33a25ce04efae19afc3a23d")
    version("0.8.1", sha256="a0674f7e320dc7ebcf51990d7fc1c0e7f7b2c335c08f5953702b5285e6c30694")
    version("0.8.0", sha256="df3b8e0b72bce38914f0fb1cd02235d8b616df9209beb14beb06bfbcaaf2e97f")
    version("0.7.1", sha256="67f840f861e5ffbe137d65a8543642d016f900b89dd035492d562ad11acf0e1e")

    depends_on("python@3:")
    depends_on("cmake")
    depends_on("gmake")
    depends_on("ninja", when="+ninjabuild")
    depends_on("openssl", when="+httpfs")
    depends_on("icu4c", when="~icu")

    # Build Options
    variant("autocomplete", default=True, description="Include autocomplete for CLI in build")
    variant("cli", default=True, description="Compile with command line client")
    variant("icu", default=False, description="Compile with bundled ICU library")
    variant("ninjabuild", default=True, description="Use GEN=ninja to build")

    # Extensions
    variant("excel", default=True, description="Include Excel formatting extension in build")
    variant("fts", default=True, description="Include FTS (full text search) support in build")
    variant("httpfs", default=True, description="Include HTTPFS (& S3) support in build")
    variant("inet", default=True, description="Include INET (ip address) support in build")
    variant("json", default=True, description="Include JSON support in build")
    variant("parquet", default=True, description="Include parquent support in build")

    # APIs
    variant("jdbc", default=False, description="Build JDBC driver (may not work)")
    variant("odbc", default=False, description="Build with ODBC driver (may not work)")
    variant("python", default=False, description="Build with Python driver (may not work)")

    def edit(self, spec, prefix):
        if "+ninjabuild" in spec:
            env["GEN"] = "ninja"
        variant_flags = [
            "autocomplete",
            "cli",
            "excel",
            "fts",
            "httpfs",
            "icu",
            "inet",
            "jdbc",
            "json",
            "odbc",
            "openssl",
            "parquet",
            "python",
        ]
        for flag in variant_flags:
            make_flag = "BUILD_" + flag.upper()
            if "+" + flag in spec:
                env[make_flag] = "1"
            elif "~" + flag in spec:
                env[make_flag] = "0"

    def url_for_version(self, version):
        return "https://github.com/duckdb/duckdb/archive/refs/tags/v{0}.tar.gz".format(version)

    def patch(self):
        # DuckDB pulls its version from a git tag, which it can't find in the tarball
        # and thus defaults to something arbitrary and breaks extensions.
        # We use the Spack version to inject it in the right place during the build

        v = self.spec.version
        if v < Version("0.10.0"):
            # Prior to version 0.10.0 we don't have DUCKDB_NORMALIZED_VERSION to consider
            filter_file(
                r'(message\(STATUS "git hash \$\{GIT_COMMIT_HASH\}, version \$\{DUCKDB_VERSION\}"\))',
                'set(DUCKDB_VERSION "v{0}")\n\\1'.format(self.spec.version),
                "CMakeLists.txt",
            )
        else:
            # Override the fallback values that are set when GIT_COMMIT_HASH doesn't work
            for i, n in enumerate(["MAJOR", "MINOR", "PATCH"]):
                filter_file("set\(DUCKDB_{0}_VERSION 0\)".format(n),
                            "set(DUCKDB_{0}_VERSION {1})".format(n, v[i]),
                            "CMakeLists.txt")
            # We still need to manually set DUCKDB_NORMALIZED_VERSION to get some helper scripts to work
            filter_file(
                r'(message\(STATUS "git hash \$\{GIT_COMMIT_HASH\}, version \$\{DUCKDB_VERSION\}, extension folder \$\{DUCKDB_NORMALIZED_VERSION\}"\))',
                'set(DUCKDB_NORMALIZED_VERSION "${DUCKDB_VERSION}")\n\\1',
                "CMakeLists.txt",
            )

    def install(self, spec, prefix):
        mkdir(prefix.bin)
        install("build/release/duckdb", prefix.bin)
