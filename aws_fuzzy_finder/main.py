import subprocess
import click
import shelve
import time
import sys

from .aws_utils import (
    get_aws_instances,
    prepare_searchable_instances
)
from .settings import (
    ENV_USE_PRIVATE_IP,
    ENV_USE_PUBLIC_DNS_OVER_IP,
    ENV_KEY_PATH,
    ENV_SSH_COMMAND_TEMPLATE,
    ENV_SSH_USER,
    ENV_TUNNEL_SSH_USER,
    ENV_TUNNEL_KEY_PATH,
    SEPARATOR,
    LIBRARY_PATH,
    CACHE_PATH,
    CACHE_EXPIRY_TIME,
    CACHE_ENABLED
)


@click.command()
@click.option('--private', 'use_private_ip', flag_value=True, help="Use private IP's")
@click.option('--key-path', help="Path to your private key")
@click.option('--user', help="Username to use with SSH command")
@click.option('--ip-only', 'ip_only', flag_value=True, help="Print chosen IP to STDOUT and exit")
@click.option('--no-cache', flag_value=True, help="Ignore and invalidate cache")
@click.option('--tunnel/--no-tunnel', help="Tunnel to another machine")
@click.option('--tunnel-key-path', default='~/.ssh/id_rsa', help="Path to your private key, default: ~/.ssh/id_rsa")
@click.option('--tunnel-user', default='ec2-user', help="User to SSH with, default: ec2-user")
def entrypoint(use_private_ip, key_path, user, ip_only, no_cache, tunnel, tunnel_key_path, tunnel_user):

    try:
        cache = None
        cache = shelve.open(CACHE_PATH)
        data = cache.get('fuzzy_finder_data')
        if CACHE_ENABLED and data and data.get('expiry') >= time.time() and not no_cache:
            boto_instance_data = data['aws_instances']
        else:
            boto_instance_data = get_aws_instances()
            if CACHE_ENABLED:
                cache['fuzzy_finder_data'] = {
                    'aws_instances': boto_instance_data,
                    'expiry': time.time() + CACHE_EXPIRY_TIME
                }
        cache.close()
    except Exception as e:
        print('Exception occured while getting cache, getting instances from AWS api: %s' % e)
        if cache:
            cache.close()
        boto_instance_data = get_aws_instances()

    searchable_instances = prepare_searchable_instances(
        boto_instance_data['Reservations'],
        use_private_ip or ENV_USE_PRIVATE_IP,
        ENV_USE_PUBLIC_DNS_OVER_IP
    )
    searchable_instances.sort(reverse=True)

    fuzzysearch_bash_command = 'echo -e "{}" | {}'.format(
        "\n".join(searchable_instances),
        LIBRARY_PATH
    )

    username = ENV_SSH_USER or user or ''
    if username:
        username = '%s@' % (username)

    key = ENV_KEY_PATH or key_path or ''
    if key:
        key = '-i %s' % (key)

    chosen_host = choice(fuzzysearch_bash_command)

    if ip_only:
        sys.stdout.write(chosen_host)
        exit(0)

    ssh_command = ENV_SSH_COMMAND_TEMPLATE.format(
        user=username,
        key=key,
        host=chosen_host,
    )

    if tunnel:
        ssh_command += " -t " + ENV_SSH_COMMAND_TEMPLATE.format(
            user=ENV_TUNNEL_SSH_USER or tunnel_user,
            key=ENV_TUNNEL_KEY_PATH or tunnel_key_path,
            host=choice(fuzzysearch_bash_command),
        )

    print(ssh_command)
    subprocess.call(ssh_command, shell=True, executable='/bin/bash')


def choice(fuzzysearch_bash_command):
    try:
        choice = subprocess.check_output(
            fuzzysearch_bash_command,
            shell=True,
            executable='/bin/bash'
        ).decode(encoding='UTF-8')
    except subprocess.CalledProcessError:
        exit(1)

    return choice.split(SEPARATOR)[1].rstrip()


if __name__ == '__main__':
    entrypoint()
