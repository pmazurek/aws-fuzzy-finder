import os
import subprocess

import boto3
import click

SEPARATOR = " @ "
ENV_SSH_USER = os.getenv('AWS_FUZZ_USER')
ENV_KEY_PATH = os.getenv('AWS_FUZZ_ENV_KEY_PATH')
ENV_USE_PRIVATE_IP = os.getenv('AWS_FUZZ_PRIVATE_IP')
ENV_SSH_COMMAND_TEMPLATE = os.getenv('AWS_FUZZ_SSH_COMMAND_TEMLPATE', "ssh {user}@{host} -i {key}")


@click.command()
@click.option('--private', 'use_private_ip', flag_value=True, help="Use private IP's")
@click.option('--key-path', default='~/.ssh/id_rsa', help="Path to your private key, default: ~/.ssh/id_rsa")
@click.option('--user', default='ec2-user', help="User to SSH with, default: ec2-user")
def entrypoint(use_private_ip, key_path, user):
    client = boto3.client('ec2')
    output = client.describe_instances()
    pretty_instances = []

    for reservation in output['Reservations']:
        for instance in reservation['Instances']:
            if instance['State']['Name'] != 'running':
                continue

            instance_data = {
                'public_ip': instance.get('PublicIpAddress', ''),
                'private_ip': instance['PrivateIpAddress'],
                'tags': instance['Tags']
            }
            pretty_instances.append(instance_data)

    def get_tag_value(tag_name, tags):
        for tag in tags:
            if tag['Key'] == tag_name:
                return tag['Value'].replace('"', '')

    instances_for_fzf = []

    for instance_data in pretty_instances:
        name = get_tag_value('Name', instance_data['tags'])
        if use_private_ip or ENV_USE_PRIVATE_IP:
            ip = instance_data['private_ip']
        else:
            ip = instance_data['public_ip'] or instance_data['private_ip']
        instances_for_fzf.append("{}{}{}".format(
            name,
            SEPARATOR,
            ip
        ))

    cmd = 'echo -e "{}" | fzf'.format("\n".join(instances_for_fzf))
    choice = subprocess.check_output(cmd, shell=True, executable='/bin/bash')
    choice = choice.decode(encoding='UTF-8')
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
