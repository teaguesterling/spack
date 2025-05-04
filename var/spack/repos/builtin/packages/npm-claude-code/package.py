# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *

class NpmClaudeCode(Package):
    """Claude Code is an agentic coding tool that lives in your terminal."""

    homepage = "https://docs.anthropic.com/en/docs/agents-and-tools/claude-code/overview"
    url = "https://registry.npmjs.org/@anthropic-ai/claude-code/-/claude-code-0.2.100.tgz"

    maintainers("teaguesterling")

    license("OTHER", checked_by="teaguesterling")

    version("0.2.100", sha256="844e341f636f779e696bc0db285bc7bfe57842a1", expand=False)

    # FIXME: Add dependencies if required.
    depends_on("node-js@18:")
    depends_on("git@2.23:")
    depends_on("ripgrep")

    depends_on("npm", type="build")

    def install(self, spec, prefix):
        npm = which("npm")
        npm("install", "-g", self.stage.archive_file)
