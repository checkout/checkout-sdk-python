"""Checks the release artifacts in dist/ before they are handed to the publish job.

Fails unless the directory holds exactly the wheel and the sdist of the expected version,
both archives contain only the entries the package is meant to ship, and the version in
the metadata and in checkout_sdk/properties.py matches. Standard library only, so it adds
nothing to the release job's locked dependencies.

Usage: python -I .github/scripts/verify_dist.py <dist dir> <version>
"""
import email.parser
import pathlib
import sys
import tarfile
import zipfile

PACKAGE = 'checkout_sdk'


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


def main(dist_dir, version):
    dist = pathlib.Path(dist_dir)
    wheel = dist / f'{PACKAGE}-{version}-py3-none-any.whl'
    sdist = dist / f'{PACKAGE}-{version}.tar.gz'
    found = sorted(path.name for path in dist.iterdir())
    if found != sorted([wheel.name, sdist.name]):
        fail(f'{dist}: found {found}, expected exactly {sorted([wheel.name, sdist.name])}')
    print(f'{wheel.name}: {check_wheel(wheel, version)} entries OK')
    print(f'{sdist.name}: {check_sdist(sdist, version)} entries OK')


if __name__ == '__main__':
    if len(sys.argv) != 3:
        fail('usage: verify_dist.py <dist dir> <version>')
    main(sys.argv[1], sys.argv[2])
