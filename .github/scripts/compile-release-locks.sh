#!/usr/bin/env bash
# Regenerates the hash-locked requirements of .github/workflows/build-release.yml:
#   requirements-release-test.txt   from requirements-ci.txt and PIP below
#   requirements-release-build.txt  from BUILD_TOOLS and PIP below
# Resolves inside linux/amd64 CPython 3.10, the interpreter and platform of the release job,
# so environment markers and wheel tags match what the runner installs. Requires Docker.
# Existing pins are kept; pass --upgrade to move every package to its latest version.
# Usage, from the repository root: bash .github/scripts/compile-release-locks.sh [--upgrade]
set -euo pipefail

# setuptools and wheel must satisfy [build-system] requires in pyproject.toml: the build job
# runs python -m build --no-isolation, which fails if the installed versions do not.
BUILD_TOOLS='build==1.6.1
setuptools==84.2.1
wheel==0.48.0'
PIP='pip==26.3'

cd "$(dirname "$0")/../.."

docker run --rm --platform linux/amd64 -v "$PWD":/src -w /src \
  -e CUSTOM_COMPILE_COMMAND="bash .github/scripts/compile-release-locks.sh" \
  -e BUILD_TOOLS="$BUILD_TOOLS" -e PIP="$PIP" -e EXTRA_ARGS="${1:-}" \
  python:3.10-slim bash -euo pipefail -c '
    pip install --quiet --root-user-action=ignore pip-tools==7.6.2
    compile() {
      pip-compile --quiet --generate-hashes --allow-unsafe --strip-extras --no-emit-index-url \
        --pip-args="--only-binary :all:" $EXTRA_ARGS "$@"
    }
    printf "%s\n" "$PIP" | compile -o requirements-release-test.txt requirements-ci.txt -
    printf "%s\n" "$BUILD_TOOLS" "$PIP" | compile -o requirements-release-build.txt -
  '
