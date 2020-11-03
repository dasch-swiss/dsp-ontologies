load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_archive")
http_archive(
    name = "rules_python",
    url = "https://github.com/bazelbuild/rules_python/releases/download/0.1.0/rules_python-0.1.0.tar.gz",
    sha256 = "b6d46438523a3ec0f3cead544190ee13223a52f6a6765a29eae7b7cc24cc83a0",
)

load("@rules_python//python/legacy_pip_import:pip.bzl", "pip_import", "pip_repositories")

# Create a central repo that knows about the dependencies needed for requirements.txt.
pip_import(   # or pip3_import
   name = "my_deps",
   requirements = "//:requirements.txt",
)

# Load the central repo's install function from its `//:requirements.bzl` file, and call it.
load("@my_deps//:requirements.bzl", "pip_install")
pip_install()