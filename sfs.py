import os
import logging
import shutil
import glob
from subprocess import run

from project import package_name, name
from hooks import pre_squash_copy_hook, pre_squash_hook, post_squash_hook

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


MKSQUASHFS_OPTS = [
    '-comp', 'lzo',
    '-Xcompression-level', '9',
    '-noappend',
    '-always-use-fragments',
    '-action', 'guid(1000, 1000) @ name(*)',
    '-action', 'exclude @ name(.empty) && filesize(0)'
]

if os.path.isfile('mksquashfs.actions'):
    logger.debug('using mksquashfs.actions')
    MKSQUASHFS_OPTS += ['-action-file', 'mksquashfs.actions']

def build_sfs():
    sfs_data_path = f".build/{package_name}/squashfs-data"

    os.makedirs(sfs_data_path, exist_ok=True)
    shutil.rmtree(sfs_data_path, ignore_errors=True)

    pre_squash_copy_hook()

    for path in glob.glob("package-rootfs*"):
        if os.path.isdir(path):
            shutil.copytree(f'{path}/.', sfs_data_path,
                            dirs_exist_ok=True, symlinks=True)

    if os.path.isdir('tcos'):
        shutil.copytree('tcos', f'{sfs_data_path}/opt/{name}/tcos')

    if os.path.isdir('schema'):
        shutil.copytree('schema', f'{sfs_data_path}/tcos/schema')

    if os.path.isdir('package-metadata'):
        shutil.copytree('package-metadata',
                        f'{sfs_data_path}/tcos/package-metadata',
                        dirs_exist_ok=True)

    os.makedirs(f'{sfs_data_path}/tcos/changelogs', exist_ok=True)
    shutil.copy2('debian/changelog',
                 f'{sfs_data_path}/tcos/changelogs/{package_name}.changelog')

    pre_squash_hook()

    run(['mksquashfs', sfs_data_path,
        f'.build/{package_name}/{name}.sfs', *MKSQUASHFS_OPTS])
    post_squash_hook()

