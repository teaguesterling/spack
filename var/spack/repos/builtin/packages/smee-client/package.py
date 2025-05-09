# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import json
import os

import llnl.util.filesystem as fs

from spack.build_systems.npm import NpmPackage
from spack.error import InstallError
from spack.package import *


class SmeeClient(NpmPackage):
    """
    Client and CLI for smee.io, a service that delivers webhooks to your
    local development environment.
    """

    homepage = "https://smee.io"
    url = "https://registry.npmjs.org/smee-client/-/smee-client-3.1.1.tgz"
    git = "https://github.com/probot/smee-client.git"

    maintainers("alecbcs", "teaguesterling")

    license("ISC")

    version("3.1.1", sha256="4c8725f4e8a423ed32865e345575e4c54d00a41029d8548ede2314da70209c7a")
    version("2.0.4", sha256="b0c959f52e384bbd3f913955cb68102fef11d85b7cc8e5a83404ee325f1ccfe4")
    version("2.0.3", sha256="98ca658cf3214c5116651f2a788c793bc2fe76543f24ada20e8751fcf1de8e1a")
    version("1.2.3", sha256="b9afff843fc7a3c2b5d6659acf45357b5db7a739243b99f6d18a9b110981a328")

    # Additional build dependencies beyond the default npm and node-js
    depends_on("typescript", type="build")

    @property
    def build_args(self):
        """Allow tsc to fail with typing "errors" which don't affect results."""
        return ["--ignore-scripts"]  # Skip scripts during install

    @property
    def build_directory(self):
        """Return the directory containing the package.json."""
        return self.stage.source_path

    def build(self, spec, prefix):
        # Use the standard build phase from npm.py, then run build script manually
        super().build(spec, prefix)

        # Create a basic tsconfig.json file if it doesn't exist
        tsconfig_path = os.path.join(self.build_directory, "tsconfig.json")
        if not os.path.exists(tsconfig_path):
            tsconfig = {
                "compilerOptions": {
                    "target": "es2018",
                    "module": "commonjs",
                    "outDir": "./lib",
                    "rootDir": "./src",
                    "strict": True,
                    "esModuleInterop": True,
                },
                "include": ["src/**/*"],
                "exclude": ["node_modules", "**/*.test.ts"],
            }
            with open(tsconfig_path, "w") as f:
                json.dump(tsconfig, f, indent=2)

        # Run the build script with special error handling
        npm = which("npm", required=True)
        with fs.working_dir(self.build_directory):
            output = npm("run", "build", output=str, error=str, fail_on_error=False)
            if npm.returncode not in (0, 2):
                raise InstallError(output)
