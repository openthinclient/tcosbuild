import os
import shutil

from pathlib import Path

from project import package_name, name, build_path
from util import shell

COMPATIBILITY_LEVEL = 13
TARGET_ARCH = 'amd64'

def build_deb():
    debian_package_path = Path(f'.build/{package_name}/debian-package')
    debian_meta_dir_path = debian_package_path / 'debian'

    debian_meta_dir_path.mkdir(parents=True)

    shutil.copy2(build_path / 'changelog', debian_meta_dir_path)
    shutil.copy2('debian/control', debian_meta_dir_path)
    shell(f'echo {COMPATIBILITY_LEVEL} > {debian_meta_dir_path}/compat')

    shutil.copytree(build_path / 'package-data',
                    debian_meta_dir_path / name,
                    dirs_exist_ok=True)

    oldpwd = os.getcwd()
    os.chdir(debian_package_path)

    shell("fakeroot dh_testdir")
    shell("fakeroot dh_testroot")
    shell("fakeroot dh_link")
    shell("fakeroot dh_strip")
    shell("fakeroot dh_compress")
    shell("fakeroot dh_fixperms")
    shell("fakeroot dh_installdeb")
    shell("fakeroot dh_gencontrol")
    shell("fakeroot dh_md5sums" )
    shell("fakeroot dh_builddeb -- -Zgzip")

    os.chdir(oldpwd)

    package_arch = f'{package_name}_{TARGET_ARCH}'
    shutil.copy2(build_path / f'{package_arch}.deb', '.build')

    shell(f'cd .build && md5sum {package_arch}.deb > {package_arch}.deb.md5')

    shutil.copy2(debian_meta_dir_path / 'changelog', f'.build/{name}.changelog')

    shell(f'cd {debian_package_path} &&'
          f' dpkg-genchanges -q -b > ../../{package_arch}.changes')

