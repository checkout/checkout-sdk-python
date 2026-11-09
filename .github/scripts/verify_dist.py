"""Checks the release artifacts in dist/ before they are handed to the publish job.

Fails unless the directory holds exactly the wheel and the sdist of the expected version,
both archives contain only the entries the package is meant to ship, and the version in
the metadata and in checkout_sdk/properties.py matches. Standard library only, so it adds
nothing to the release job's locked dependencies.

Run from the repository root: python -I .github/scripts/verify_dist.py <version>
"""
import email.parser
import pathlib
import re
import sys
import tarfile
import zipfile

PACKAGE = 'checkout_sdk'
DIST = pathlib.Path('dist')
VERSION_PATTERN = re.compile(r'\d+\.\d+\.\d+((a|b|rc)\d+)?(\.dev\d+)?', re.ASCII)


def fail(message):
    sys.exit(f'verify_dist: {message}')


def read_metadata(raw):
    return email.parser.Parser().parsestr(raw.decode('utf-8'))


def check_metadata(metadata, version, source):
    if metadata['Name'] != PACKAGE:
        fail(f'{source}: Name is {metadata["Name"]!r}, expected {PACKAGE!r}')
    if metadata['Version'] != version:
        fail(f'{source}: Version is {metadata["Version"]!r}, expected {version!r}')


def check_properties(raw, version, source):
    expected = f'VERSION = "{version}"'
    if expected not in raw.decode('utf-8'):
        fail(f'{source}: checkout_sdk/properties.py does not contain {expected}')


def check_wheel(path, version):
    allowed = {PACKAGE, f'{PACKAGE}-{version}.dist-info'}
    with zipfile.ZipFile(path) as wheel:
        names = wheel.namelist()
        unexpected = sorted({name.split('/')[0] for name in names} - allowed)
        if unexpected:
            fail(f'{path.name}: unexpected top-level entries {unexpected}')
        check_metadata(read_metadata(wheel.read(f'{PACKAGE}-{version}.dist-info/METADATA')),
                       version, path.name)
        check_properties(wheel.read(f'{PACKAGE}/properties.py'), version, path.name)
    return len(names)


def check_sdist(path, version):
    root = f'{PACKAGE}-{version}'
    allowed = {'LICENSE.md', 'PKG-INFO', 'README.md', PACKAGE, f'{PACKAGE}.egg-info',
               'pyproject.toml', 'setup.cfg', 'setup.py'}
    with tarfile.open(path) as sdist:
        members = [member for member in sdist.getmembers() if member.name != root]
        for member in members:
            parts = member.name.split('/')
            if parts[0] != root or parts[1] not in allowed:
                fail(f'{path.name}: unexpected entry {member.name}')
            if not (member.isfile() or member.isdir()):
                fail(f'{path.name}: {member.name} is not a regular file or directory')
        check_metadata(read_metadata(sdist.extractfile(f'{root}/PKG-INFO').read()),
                       version, path.name)
        check_properties(sdist.extractfile(f'{root}/{PACKAGE}/properties.py').read(),
                         version, path.name)
    return len(members)


def main(version):
    if not VERSION_PATTERN.fullmatch(version):
        fail(f'{version!r} is not a release or dev version')
    # The version is only compared with file names; the files opened come from the listing.
    files = sorted(DIST.iterdir())
    expected = sorted([f'{PACKAGE}-{version}-py3-none-any.whl', f'{PACKAGE}-{version}.tar.gz'])
    if [path.name for path in files] != expected:
        fail(f'{DIST}: found {[path.name for path in files]}, expected exactly {expected}')
    wheel, sdist = files  # '-py3' sorts before '.tar', so the wheel comes first
    print(f'{wheel.name}: {check_wheel(wheel, version)} entries OK')
    print(f'{sdist.name}: {check_sdist(sdist, version)} entries OK')


if __name__ == '__main__':
    if len(sys.argv) != 2:
        fail('usage: verify_dist.py <version>')
    main(sys.argv[1])
