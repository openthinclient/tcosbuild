import os
import argparse

from subprocess import run

from project import build_path

DEFAULT_INSTALL_PATH = '/home/openthinclient/otc-manager-home/nfs/root'
SSH_OPTS = '-oStrictHostKeyChecking=no'

def initialize_install_arg_parser(parser: argparse.ArgumentParser):
    parser.add_argument('destination', help='user@host')
    parser.add_argument('-p', '--password', help='optional ssh password to use')
    parser.add_argument('-P', '--path', help='path to nfs root on the server')

def install(args: argparse.Namespace):
    os.chdir(build_path / 'package-data')
    sshpass = ['sshpass', '-p', args.password] if args.password else []

    remote_path = args.path or DEFAULT_INSTALL_PATH
    run([*sshpass, 'scp', '-r', '.', f'{args.destination}:/tmp/package'])

    run([*sshpass, 'ssh', args.destination,
        f'cd "{remote_path}";'
        'sudo cp -rv /tmp/package/. .;'
        'rm -rf /tmp/package'])


