import boto3
from botocore.exceptions import (
    NoRegionError,
    PartialCredentialsError,
    NoCredentialsError,
    ClientError
)

from .settings import (
    SEPARATOR,
    NO_REGION_ERROR,
    NO_CREDENTIALS_ERROR,
    WRONG_CREDENTIALS_ERROR
)


def gather_instance_data(reservations):
    instances = []

    for reservation in reservations:
        for instance in reservation['Instances']:
            if instance['State']['Name'] != 'running':
                continue

            # skipping not named instances
            if 'Tags' not in instance:
                continue

            instance_data = {
                'public_ip': instance.get('PublicIpAddress', ''),
                'private_ip': instance['PrivateIpAddress'],
                'tags': instance['Tags']
            }
            instances.append(instance_data)
    return instances


def get_tag_value(tag_name, tags):
    for tag in tags:
        if tag['Key'] == tag_name:
            return tag['Value'].replace('"', '')


def get_aws_instances():
    try:
        return boto3.client('ec2').describe_instances()
    except NoRegionError:
        print(NO_REGION_ERROR)
        exit(1)
    except (PartialCredentialsError, NoCredentialsError):
        print(NO_CREDENTIALS_ERROR)
        exit(1)
    except ClientError:
        print(WRONG_CREDENTIALS_ERROR)
        exit(1)


def prepare_searchable_instances(reservations, use_private_ip):
    instance_data = gather_instance_data(reservations)
    searchable_instances = []
    for instance in instance_data:
        name = get_tag_value('Name', instance['tags'])
        if use_private_ip:
            ip = instance['private_ip']
        else:
            ip = instance['public_ip'] or instance['private_ip']
        searchable_instances.append("{}{}{}".format(
            name,
            SEPARATOR,
            ip
        ))
    return searchable_instances
