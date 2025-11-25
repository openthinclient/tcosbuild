import os
import argparse

from subprocess import run

from project import build_path

DEFAULT_INSTALL_PATH = '/home/openthinclient/otc-manager-home/nfs/root'
DEFAULT_CLIENT_INSTALL_PATH = '/'
SSH_OPTS = ['-oStrictHostKeyChecking=no', '-oUserKnownHostsFile=/dev/null']

class Installer:
    def __init__(self, args: argparse.Namespace) -> None:
        self.args = args
        self.sshpass_prefix = ['sshpass', '-p', args.password] \
                              if args.password else []

    @staticmethod
    def initialize_arg_parser(parser: argparse.ArgumentParser):
        parser.add_argument('destination', help='user@host')
        parser.add_argument('-p', '--password', help='optional ssh password to use')
        parser.add_argument('-P', '--path', help='destination path')

    def _install(self, path):
        run([*self.sshpass_prefix,
            'rsync', '-ra', '.',
            f'{self.args.destination}:/tmp/package',
            '-e', 'ssh ' + ' '.join(SSH_OPTS)])

        run([*self.sshpass_prefix,
            'ssh', *SSH_OPTS, self.args.destination,
            f'cd "{path}";'
            'sudo cp -rv /tmp/package/. .;'
            'rm -rf /tmp/package'])

    def install(self):
        os.chdir(build_path / 'package-data')
        remote_path = self.args.path or DEFAULT_INSTALL_PATH
        self._install(remote_path)

    def client_install(self):
        os.chdir(build_path / 'squashfs-data')
        remote_path = self.args.path or DEFAULT_CLIENT_INSTALL_PATH
        self._install(remote_path)

