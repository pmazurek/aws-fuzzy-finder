import subprocess
import sys
import click
import redis
import pickle

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
    LIBRARY_PATH,
    ENV_USE_REDIS,
    REDIS_HOST,
    REDIS_PORT,
    REDIS_DB,
    REDIS_EXPIRE,
    REDIS_KEY
)


@click.command()
@click.option('--private', 'use_private_ip', flag_value=True, help="Use private IP's")
@click.option('--key-path', default='~/.ssh/id_rsa', help="Path to your private key, default: ~/.ssh/id_rsa")
@click.option('--user', default='ec2-user', help="User to SSH with, default: ec2-user")
@click.option('--ip-only', 'ip_only', flag_value=True, help="Print chosen IP to STDOUT and exit")
@click.option('--use-redis', 'use_redis', flag_value=True, help="use redis for caching, default: false")
@click.option('--rh', default='localhost', help="redis host, default: localhost")
@click.option('--rp', default='6379', help="redis port, default: 6379")
@click.option('--rd', default='0', help="redis db id, default: 0")
@click.option('--re', default='300', help="redis expire time in seconds, default: 300")
@click.option('--rk', default='aws_fuzzy_finder_data', help="redis key to store data, default: aws_fuzzy_finder_data")
def entrypoint(use_private_ip, key_path, user, ip_only, use_redis, rh, rp, rd, re, rk):
    if ENV_USE_REDIS or use_redis:
        try:
            r_server = redis.Redis(REDIS_HOST or rh, port=REDIS_PORT or rp, db=REDIS_DB or rd)
            if not r_server.exists(REDIS_KEY or rk):
                boto_instance_data = get_aws_instances()
                r_server.setex(REDIS_KEY or rk, pickle.dumps(boto_instance_data), REDIS_EXPIRE or re)
            else:
                boto_instance_data = pickle.loads(r_server.get(REDIS_KEY or rk))
        except redis.ConnectionError as redis_err:
            print("Redis connection error: {}".format(redis_err))
            exit(1)
    else:
        boto_instance_data = get_aws_instances()

    searchable_instances = prepare_searchable_instances(
        boto_instance_data['Reservations'],
        use_private_ip or ENV_USE_PRIVATE_IP
    )
    searchable_instances.sort(reverse=True)

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
