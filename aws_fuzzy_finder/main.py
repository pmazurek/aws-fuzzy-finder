import subprocess
import click
import shelve
import time
import sys
import os

from .aws_utils import (
    get_aws_instances,
    prepare_searchable_instances
)
from .settings import (
    ENV_USE_PRIVATE_IP,
    ENV_USE_PUBLIC_DNS_OVER_IP,
    ENV_KEY_PATH,
    ENV_SSH_COMMAND_TEMPLATE,
    ENV_SSM_COMMAND_TEMPLATE,
    ENV_USE_SSM,
    ENV_SSH_USER,
    ENV_TUNNEL_SSH_USER,
    ENV_TUNNEL_KEY_PATH,
    AWS_REGIONS,
    AWS_DEFAULT_PROFILE,
    SEPARATOR,
    LIBRARY_PATH,
    CACHE_DIR,
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
@click.option('--ssm', 'use_ssm', flag_value=True, help="Tell the tool internally find the instance id and use AWS SSM")
@click.option('--id-only', 'id_only', flag_value=True, help="Print chosen Instance ID to STDOUT and exit")
def entrypoint(use_private_ip, key_path, user, ip_only, no_cache, tunnel, tunnel_key_path, tunnel_user, use_ssm, id_only):
    if not os.path.exists(CACHE_DIR):
        os.makedirs(CACHE_DIR)

    try:
        cache = None
        cache = shelve.open(CACHE_PATH)
        data = cache.get('fuzzy_finder_data')
        # if you have set your cache to never expire
        if CACHE_ENABLED and data and CACHE_EXPIRY_TIME == 0 and not no_cache:
            boto_instance_data = data['aws_instances']
        # if you set your cache to expire, check if it has expired
        elif CACHE_ENABLED and data and data.get('expiry') >= time.time() and not no_cache:
            boto_instance_data = data['aws_instances']
        # there is no cache file or it is expired or --no-cache was used to refresh data
        else:
            boto_instance_data = {}
            for region in AWS_REGIONS:
                current_region_data = get_aws_instances(region)
                boto_instance_data[region] = current_region_data
            if CACHE_ENABLED:
                cache['fuzzy_finder_data'] = {
                    'aws_instances': boto_instance_data,
                    'expiry': time.time() + CACHE_EXPIRY_TIME
                }
        cache.close()
    except Exception as e:
        print('Exception occurred while getting cache, getting instances from AWS api: %s' % e)
        if cache:
            cache.close()
        boto_instance_data = {}
        for region in AWS_REGIONS:
            current_region_data = get_aws_instances(region)
            boto_instance_data[region] = current_region_data

    searchable_instances = prepare_searchable_instances(
        AWS_REGIONS,
        boto_instance_data,
        use_private_ip or ENV_USE_PRIVATE_IP,
        ENV_USE_PUBLIC_DNS_OVER_IP
    )
    searchable_instances.sort(reverse=True)

    fuzzysearch_bash_command = 'echo -e "{}" | {}'.format(
        "\n".join(searchable_instances),
        LIBRARY_PATH
    )

    chosen_host = choice(fuzzysearch_bash_command, use_ssm)

    if ENV_USE_SSM or use_ssm:
        if id_only:
            sys.stdout.write(chosen_host)
            exit(0)

        ssm_command = ENV_SSM_COMMAND_TEMPLATE.format(
            profile=AWS_DEFAULT_PROFILE,
            target=chosen_host,
        )
        print(ssm_command)
        subprocess.call(ssm_command, shell=True, executable='/bin/bash')
    else:
        if ip_only:
            sys.stdout.write(chosen_host)
            exit(0)

        username = ENV_SSH_USER or user or ''
        if username:
            username = '%s@' % (username)

        key = ENV_KEY_PATH or key_path or ''
        if key:
            key = '-i %s' % (key)

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


def choice(fuzzysearch_bash_command, use_ssm):
    output = ""  # used to collect the value returned
    try:
        choice = subprocess.check_output(
            fuzzysearch_bash_command,
            shell=True,
            executable='/bin/bash'
        ).decode(encoding='UTF-8')
    except subprocess.CalledProcessError:
        exit(1)

    if use_ssm:
        output = choice.split(' ')[1].replace('(', '').replace(')', '').rstrip()
    else:
        output = choice.split(SEPARATOR)[1].rstrip()
    return output


if __name__ == '__main__':
    entrypoint()
