import os
import argparse

from subprocess import run

from project import build_path

DEFAULT_INSTALL_PATH = '/home/openthinclient/otc-manager-home/nfs/root'
DEFAULT_CLIENT_INSTALL_PATH = '/'
SSH_OPTS = '-oStrictHostKeyChecking=no'

def initialize_install_arg_parser(parser: argparse.ArgumentParser):
    parser.add_argument('destination', help='user@host')
    parser.add_argument('-p', '--password', help='optional ssh password to use')
    parser.add_argument('-P', '--path', help='destination path')

def _install(destination, path, password):
    sshpass = ['sshpass', '-p', password] if password else []

    run([*sshpass, 'rsync', '-r', '.', f'{destination}:/tmp/package'])

    run([*sshpass, 'ssh', destination,
        f'cd "{path}";'
        'sudo cp -rv /tmp/package/. .;'
        'rm -rf /tmp/package'])

def install(args: argparse.Namespace):
    os.chdir(build_path / 'package-data')
    remote_path = args.path or DEFAULT_INSTALL_PATH
    _install(args.destination, remote_path, args.password)

def client_install(args: argparse.Namespace):
    os.chdir(build_path / 'squashfs-data')
    remote_path = args.path or DEFAULT_CLIENT_INSTALL_PATH
    _install(args.destination, remote_path, args.password)

