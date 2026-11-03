#!/usr/bin/env bash
# Regenerates the hash-locked requirements of .github/workflows/build-release.yml:
#   requirements-release-test.txt   from requirements-ci.txt
#   requirements-release-build.txt  from the build tool pins below
# Resolves inside linux/amd64 CPython 3.10, the interpreter and platform of the release job,
# so environment markers and wheel tags match what the runner installs. Requires Docker.
# Usage, from the repository root: bash .github/scripts/compile-release-locks.sh
set -euo pipefail

# setuptools and wheel must match [build-system] requires in pyproject.toml: the build job
# runs python -m build --no-isolation, which fails if the installed versions differ.
BUILD_TOOLS='build==1.6.1
setuptools==84.2.1
wheel==0.48.0'

cd "$(dirname "$0")/../.."

docker run --rm -i --platform linux/amd64 -v "$PWD":/src -w /src \
  -e CUSTOM_COMPILE_COMMAND="bash .github/scripts/compile-release-locks.sh" \
  python:3.10-slim bash -euo pipefail -c '
    pip install --quiet --root-user-action=ignore pip-tools==7.6.2
    compile() {
      pip-compile --quiet --generate-hashes --allow-unsafe --strip-extras --no-emit-index-url \
        --pip-args="--only-binary :all:" "$@"
    }
    compile -o requirements-release-test.txt requirements-ci.txt < /dev/null
    compile -o requirements-release-build.txt -
  ' <<< "$BUILD_TOOLS"
