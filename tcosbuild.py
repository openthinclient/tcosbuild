#!/usr/bin/env python3
import argparse
import os
import shutil
import logging

from package_data import build_package_data
from project import package_name, version, build_path
from sfs import build_sfs, build_sfs_data
from deb import build_deb
from install import Installer

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def pre_build():
    if build_path.is_dir():
        shutil.rmtree(build_path)
    os.makedirs(build_path)

    shutil.copy2('debian/changelog', build_path)
    with open(f'.build/{package_name}/changelog', 'r+') as changelog_file:
        changelog = changelog_file.readlines()
        head = changelog[0].split(' ')
        head[1] = f'({version})'
        changelog[0] = ' '.join(head)
        changelog_file.seek(0)
        changelog_file.writelines(changelog)
        changelog_file.truncate()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(title='command',
                                       dest='command',
                                       required=True)
    subparsers.add_parser('sfs', help='build sfs')
    subparsers.add_parser('deb', help='build deb')
    subparsers.add_parser('clean', help='clean build artifacts')
    install_parser = subparsers.add_parser('install', help='install to server')
    Installer.initialize_arg_parser(install_parser)
    client_install_parser = subparsers.add_parser('client_install',
                                                  help='install to client')
    Installer.initialize_arg_parser(client_install_parser)

    args = parser.parse_args()

    pre_build()
    match args.command:
        case 'sfs':
            build_sfs()
        case 'deb':
            build_sfs()
            build_package_data()
            build_deb()
        case 'clean':
            shutil.rmtree('.build')
        case 'install':
            build_sfs()
            build_package_data()
            Installer(args).install()
        case 'client_install':
            build_sfs_data()
            Installer(args).client_install()


