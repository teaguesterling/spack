# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import llnl.util.filesystem as fs

import spack.builder
import spack.package_base
import spack.phase_callbacks
import spack.spec
import spack.util.environment
import spack.util.prefix
from spack.directives import build_system, depends_on
from spack.multimethod import when

from ._checks import BuilderWithDefaults, execute_install_time_tests


class NpmPackage(spack.package_base.PackageBase):
    """Specialized class for packages built using npm."""

    #: This attribute is used in UI queries that need to know the build
    #: system base class
    build_system_class = "NpmPackage"

    #: Legacy buildsystem attribute used to deserialize and install old specs
    legacy_buildsystem = "npm"

    build_system("npm")

    with when("build_system=npm"):
        depends_on("npm", type=("build", "run"))
        depends_on("node-js", type=("build", "run"))


@spack.builder.builder("npm")
class NpmBuilder(BuilderWithDefaults):
    """The NPM builder encodes the most common way of building software with
    a package.json file. It has two phases that can be overridden, if need be:

            1. :py:meth:`~.NpmBuilder.build`
            2. :py:meth:`~.NpmBuilder.install`

    For a finer tuning you may override:

        +-----------------------------------------------+----------------------+
        | **Method**                                    | **Purpose**          |
        +===============================================+======================+
        | :py:attr:`~.NpmBuilder.build_args`            | Specify arguments    |
        |                                               | to ``npm install``   |
        +-----------------------------------------------+----------------------+
        | :py:attr:`~.NpmBuilder.check_args`            | Specify arguments    |
        |                                               | to ``npm test``      |
        +-----------------------------------------------+----------------------+
    """

    phases = ("build", "install")

    #: Names associated with package methods in the old build-system format
    legacy_methods = ("check", "installcheck")

    #: Names associated with package attributes in the old build-system format
    legacy_attributes = (
        "build_args",
        "check_args",
        "build_directory",
        "install_time_test_callbacks",
    )

    #: Callback names for install-time test
    install_time_test_callbacks = ["check"]

    def setup_build_environment(
        self, env: spack.util.environment.EnvironmentModifications
    ) -> None:
        """Set up the build environment for npm."""
        # Set npm cache directory to prevent permission issues
        npm_cache_dir = fs.join_path(self.pkg.stage.path, "npm-cache")
        env.set("npm_config_cache", npm_cache_dir)
        
        # Enable install-links for better symlinking
        env.set("npm_config_install_links", "true")
        
        # Prevent npm from trying to update itself
        env.set("npm_config_update_notifier", "false")

    @property
    def build_directory(self):
        """Return the directory containing the package.json."""
        return self.pkg.stage.source_path

    @property
    def build_args(self):
        """Arguments for ``npm install``."""
        return []

    @property
    def check_args(self):
        """Arguments for ``npm test``."""
        return []

    def build(
        self, pkg: NpmPackage, spec: spack.spec.Spec, prefix: spack.util.prefix.Prefix
    ) -> None:
        """Run npm install in the source directory."""
        with fs.working_dir(self.build_directory):
            # Use npm from module (injected by setup_dependent_package in npm package)
            # or find it on PATH if not available
            npm = getattr(pkg.module, "npm", None) or which("npm", required=True)
            
            # Run npm install to download dependencies
            npm("install", *self.build_args)
            
            # If there's a build script in package.json, run it
            if hasattr(pkg, "has_build_script") and pkg.has_build_script:
                npm("run", "build")
            elif self._has_script("build"):
                try:
                    npm("run", "build", fail_on_error=False)
                except Exception as e:
                    tty.warn(f"Build script failed but continuing: {str(e)}")

    def install(
        self, pkg: NpmPackage, spec: spack.spec.Spec, prefix: spack.util.prefix.Prefix
    ) -> None:
        """Install the package to the prefix."""
        with fs.working_dir(self.build_directory):
            # Use npm from module (injected by setup_dependent_package in npm package)
            # or find it on PATH if not available
            npm = getattr(pkg.module, "npm", None) or which("npm", required=True)
            
            # Handle tarballs - install globally with npm
            if self._is_tarball():
                # For tarballs, use npm install -g approach
                npm("install", "--global", "--prefix", prefix, self.pkg.stage.archive_file)
            else:
                # For source installs:
                # Try to use npm's built-in installation if package has package.json
                if os.path.exists(os.path.join(self.build_directory, "package.json")):
                    # Use npm install with the prefix explicitly set
                    npm("install", "--global", "--prefix", prefix, ".")
                else:
                    # Fallback to manual installation
                    # 1. Create the destination directories
                    fs.mkdirp(prefix.bin)
                    fs.mkdirp(prefix.lib)
                    
                    # 2. Install the package to the lib/node_modules directory
                    module_dir = os.path.join(prefix.lib, "node_modules", self._get_package_name())
                    fs.mkdirp(module_dir)
                    
                    # Install the package files
                    self._install_package_files(module_dir)
                    
                    # Create symlinks for bin entries in package.json
                    self._create_bin_links(prefix)

    def check(self):
        """Run the package tests."""
        with fs.working_dir(self.build_directory):
            if self._has_script("test"):
                # Use npm from module (injected by setup_dependent_package in npm package)
                # or find it on PATH if not available
                npm = getattr(self.pkg.module, "npm", None) or which("npm", required=True)
                npm("test", *self.check_args)

    spack.phase_callbacks.run_after("install")(execute_install_time_tests)

    def _has_script(self, script_name):
        """Check if package.json has the given script."""
        import json
        package_json = os.path.join(self.build_directory, "package.json")
        if os.path.isfile(package_json):
            with open(package_json) as f:
                try:
                    data = json.load(f)
                    return (
                        "scripts" in data 
                        and script_name in data["scripts"]
                    )
                except (json.JSONDecodeError, KeyError):
                    pass
        return False

    def _get_package_name(self):
        """Get the package name from package.json."""
        import json
        package_json = os.path.join(self.build_directory, "package.json")
        if os.path.isfile(package_json):
            with open(package_json) as f:
                try:
                    data = json.load(f)
                    return data.get("name", self.pkg.name)
                except (json.JSONDecodeError, KeyError):
                    pass
        return self.pkg.name

    def _is_tarball(self):
        """Check if we're installing from a tarball."""
        return hasattr(self.pkg, "stage") and self.pkg.stage.archive_file is not None

    def _install_package_files(self, module_dir):
        """Install package files to the module directory."""
        # Files to copy (standard npm package files)
        standard_files = [
            "package.json",
            "README.md",
            "LICENSE",
            "index.js",
            "dist",
            "lib",
            "src",
            "bin"
        ]
        
        # Copy standard files if they exist
        for f in standard_files:
            src = os.path.join(self.build_directory, f)
            if os.path.exists(src):
                if os.path.isfile(src):
                    fs.install(src, os.path.join(module_dir, f))
                elif os.path.isdir(src):
                    fs.install_tree(src, os.path.join(module_dir, f))
        
        # Copy node_modules if it exists and contains production dependencies
        node_modules_path = os.path.join(self.build_directory, "node_modules")
        if os.path.isdir(node_modules_path):
            fs.install_tree(node_modules_path, os.path.join(module_dir, "node_modules"))

    def _create_bin_links(self, prefix):
        """Create symlinks for bin entries in package.json."""
        import json
        package_json = os.path.join(self.build_directory, "package.json")
        
        if os.path.isfile(package_json):
            with open(package_json) as f:
                try:
                    data = json.load(f)
                    bin_entries = data.get("bin", {})
                    
                    # Handle string bin entry
                    if isinstance(bin_entries, str):
                        bin_entries = {data.get("name", self.pkg.name): bin_entries}
                    
                    # Create symlinks for each bin entry
                    for bin_name, bin_path in bin_entries.items():
                        # Source is the actual script in the node_modules directory
                        pkg_name = self._get_package_name()
                        src = os.path.join(prefix.lib, "node_modules", pkg_name, bin_path)
                        
                        # Destination is in the bin directory
                        dest = os.path.join(prefix.bin, bin_name)
                        
                        # Create the symlink
                        if os.path.isfile(src):
                            # Make the script executable
                            fs.set_executable(src)
                            
                            # Create the symlink
                            fs.symlink(os.path.relpath(src, os.path.dirname(dest)), dest)
                except (json.JSONDecodeError, KeyError):
                    pass