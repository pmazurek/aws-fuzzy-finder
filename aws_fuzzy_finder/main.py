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
    SEPARATOR,
    LIBRARY_PATH
)


@click.command()
@click.option('--private', 'use_private_ip', flag_value=True, help="Use private IP's")
@click.option('--key-path', default='~/.ssh/id_rsa', help="Path to your private key, default: ~/.ssh/id_rsa")
@click.option('--user', default='ec2-user', help="User to SSH with, default: ec2-user")
@click.option('--ip-only', 'ip_only', flag_value=True, help="Print chosen IP to STDOUT and exit")
def entrypoint(use_private_ip, key_path, user, ip_only):

    boto_instance_data = get_aws_instances()
    searchable_instances = prepare_searchable_instances(
        boto_instance_data['Reservations'],
        use_private_ip or ENV_USE_PRIVATE_IP
    )

    fuzzysearch_bash_command = 'echo -e "{}" | {}'.format(
        "\n".join(searchable_instances),
        LIBRARY_PATH
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

    if ip_only:
        sys.stdout.write(chosen_ip)
        exit(0)
    else:
        ssh_command = ENV_SSH_COMMAND_TEMPLATE.format(
            user=ENV_SSH_USER or user,
            key=ENV_KEY_PATH or key_path,
            host=chosen_ip,
        )
        # print the ssh command before executing, so that it's clear what is being done
        print(ssh_command)
        subprocess.call(ssh_command, shell=True, executable='/bin/bash')

if __name__ == '__main__':
    entrypoint()
