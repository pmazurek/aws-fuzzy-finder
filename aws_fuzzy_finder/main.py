import os
import subprocess
import sys

import click

from .aws_utils import (
    get_aws_instances,
    prepare_searchable_instances
)
from .settings import (
    ENV_USE_PRIVATE_IP,
    ENV_KEY_PATH,
    ENV_SSH_COMMAND_TEMPLATE,
    ENV_SSH_USER,
    SEPARATOR
)


def get_os_library():
    if sys.platform.startswith('linux'):
        lib = 'fzf-0.12.1-linux_386'
    elif sys.platform == 'darwin':
        lib = 'fzf-0.12.1-darwin_386'
    else:
        print('Currently only MAC OS and Linux are supported, exiting.')
        exit(1)

    return '{}/{}'.format(
        os.path.dirname(os.path.abspath(__file__)),
        lib
    )


@click.command()
@click.option('--private', 'use_private_ip', flag_value=True, help="Use private IP's")
@click.option('--key-path', default='~/.ssh/id_rsa', help="Path to your private key, default: ~/.ssh/id_rsa")
@click.option('--user', default='ec2-user', help="User to SSH with, default: ec2-user")
def entrypoint(use_private_ip, key_path, user):

    boto_instance_data = get_aws_instances()
    searchable_instances = prepare_searchable_instances(
        boto_instance_data['Reservations'],
        use_private_ip or ENV_USE_PRIVATE_IP
    )

    fuzzysearch_bash_command = 'echo -e "{}" | {}'.format(
        "\n".join(searchable_instances),
        get_os_library()
    )

    try:
        choice = subprocess.check_output(
            fuzzysearch_bash_command,
            shell=True,
            executable='/bin/bash'
        ).decode(encoding='UTF-8')
    except subprocess.CalledProcessError:
        exit(1)

    chosen_ip = choice.split(SEPARATOR)[1].rstrip()
    ssh_command = ENV_SSH_COMMAND_TEMPLATE.format(
        user=ENV_SSH_USER or user,
        key=ENV_KEY_PATH or key_path,
        host=chosen_ip,
    )
    print(ssh_command)
    subprocess.call(ssh_command, shell=True, executable='/bin/bash')

if __name__ == '__main__':
    entrypoint()
