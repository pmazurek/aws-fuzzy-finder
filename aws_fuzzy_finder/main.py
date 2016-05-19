import os
import subprocess
import sys

import boto3
from botocore.exceptions import NoRegionError, PartialCredentialsError, NoCredentialsError

import click

from .aws_utils import gather_instance_data, get_tag_value

SEPARATOR = " @ "
ENV_SSH_USER = os.getenv('AWS_FUZZ_USER')
ENV_KEY_PATH = os.getenv('AWS_FUZZ_KEY_PATH')
ENV_USE_PRIVATE_IP = os.getenv('AWS_FUZZ_PRIVATE_IP')
ENV_SSH_COMMAND_TEMPLATE = os.getenv('AWS_FUZZ_SSH_COMMAND_TEMLPATE', "ssh {user}@{host} -i {key}")


def get_aws_instances():

    try:
        client = boto3.client('ec2')
        boto_instance_data = client.describe_instances()
    except NoRegionError:
        print('No AWS region specified.')
        print('Specify region in your boto config or add a "AWS_DEFAULT_REGION" environment variable.')
        print('$ export AWS_DEFAULT_REGION="<your_region_code>"')
        print('For more info visit:')
        print('http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-regions-availability-zones.html#'
              'concepts-available-regions')
        exit(1)
    except (PartialCredentialsError, NoCredentialsError):
        print('No AWS credentials specified.')
        print('Make sure to set your aws_access_key_id, aws_secret_access_key and region in your boto config')
        print('as described here: http://boto3.readthedocs.io/en/latest/guide/configuration.html')
        exit(1)

    return boto_instance_data


@click.command()
@click.option('--private', 'use_private_ip', flag_value=True, help="Use private IP's")
@click.option('--key-path', default='~/.ssh/id_rsa', help="Path to your private key, default: ~/.ssh/id_rsa")
@click.option('--user', default='ec2-user', help="User to SSH with, default: ec2-user")
def entrypoint(use_private_ip, key_path, user):

    boto_instance_data = get_aws_instances()
    instance_data = gather_instance_data(boto_instance_data['Reservations'])

    searchable_instances = []
    for instance in instance_data:
        name = get_tag_value('Name', instance['tags'])
        if use_private_ip or ENV_USE_PRIVATE_IP:
            ip = instance['private_ip']
        else:
            ip = instance['public_ip'] or instance['private_ip']
        searchable_instances.append("{}{}{}".format(
            name,
            SEPARATOR,
            ip
        ))

    if sys.platform.startswith('linux'):
        lib = 'fzf-0.12.1-linux_386'
    elif sys.platform == 'darwin':
        lib = 'fzf-0.12.1-darwin_386'
    else:
        print('Currently only MAC OS and Linux are supported, exiting.')
        exit(1)

    lib_path = '{}/{}'.format(
        os.path.dirname(os.path.abspath(__file__)),
        lib
    )
    fuzzysearch_bash_command = 'echo -e "{}" | {}'.format(
        "\n".join(searchable_instances),
        lib_path
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
