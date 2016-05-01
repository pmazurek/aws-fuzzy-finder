import os
import subprocess

import boto3

SEPARATOR = " @ "
SSH_USER = os.getenv('AWS_FUZZ_USER', 'ec2-user')
KEY_PATH = os.getenv('AWS_FUZZ_KEY_PATH', '~/.ssh/id_rsa')


def entrypoint():
    client = boto3.client('ec2')
    output = client.describe_instances()
    pretty_instances = []

    for reservation in output['Reservations']:
        for instance in reservation['Instances']:
            instance_data = {
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
        ip = instance_data['private_ip']
        instances_for_fzf.append("{}{}{}".format(
            name,
            SEPARATOR,
            ip
        ))

    cmd = 'echo -e "{}" | fzf'.format("\n".join(instances_for_fzf))
    choice = subprocess.check_output(cmd, shell=True, executable='/bin/bash')
    chosen_ip = choice.split(SEPARATOR)[1].rstrip()

    ssh_command = "ssh {user}@{host} -i {key}".format(
        user=SSH_USER,
        key=KEY_PATH,
        host=chosen_ip,
    )

    subprocess.call(ssh_command, shell=True, executable='/bin/bash')

if __name__ == '__main__':
    entrypoint()
