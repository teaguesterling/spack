# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Duckdb(MakefilePackage):
    """DuckDB is an in-process SQL OLAP Database Management System."""

    homepage = "https://duckdb.org"
    url = "https://github.com/duckdb/duckdb/archive/refs/tags/v0.8.1.tar.gz"
    git = "https://github.com/duckdb/duckdb.git"

    version("master", branch="master")
    version("0.8.1", sha256="a0674f7e320dc7ebcf51990d7fc1c0e7f7b2c335c08f5953702b5285e6c30694")
    version("0.8.0", sha256="df3b8e0b72bce38914f0fb1cd02235d8b616df9209beb14beb06bfbcaaf2e97f")
    version("0.7.1", sha256="67f840f861e5ffbe137d65a8543642d016f900b89dd035492d562ad11acf0e1e")

    depends_on("python@3:")

    variant("autocomplete", default=True)
    variant("icu", default=True)
    variant("json", default=True)
    variant("httpfs", default=True)
    variant("excel", default=True)
    variant("openssl", default=True)
    variant("odbc", default=False)
    variant("jdbc", default=False)
    variant("fts", default=True)
    variant("parquet", default=True)

    def edit(self, spec, prefix):
        extensions = [
            "autocomplete",
            "icu",
            "json",
            "httpfs",
            "excel",
            "openssl",
            "odbc",
            "jdbc",
            "fts",
            "parquet",
        ]
        for flag in extensions:
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
        filter_file(
            r'(message\(STATUS "git hash \$\{GIT_COMMIT_HASH\}, version \$\{DUCKDB_VERSION\}"\))',
            'set(DUCKDB_VERSION "v{0}")\n\\1'.format(self.spec.version),
            "CMakeLists.txt",
        )

    def install(self, spec, prefix):
        mkdir(prefix.bin)
        install("build/release/duckdb", prefix.bin)
