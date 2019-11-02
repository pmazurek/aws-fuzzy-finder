import os
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


def gather_instance_data(aws_regions, instance_data):
    instances = []
    for region in aws_regions:
        reservations = instance_data[region]
        for reservation in reservations['Reservations']:
            for instance in reservation['Instances']:
                if instance['State']['Name'] != 'running':
                    continue

                data = {
                    'public_ip': instance.get('PublicIpAddress', ''),
                    'private_ip': instance['PrivateIpAddress'],
                    'public_dns': instance.get('PublicDnsName', ''),
                    'instance_id': instance.get('InstanceId'),
                    'tags': instance.get('Tags', []),
                }
                instances.append(data)
    return instances


def get_tag_value(tag_name, tags):
    for tag in tags:
        if tag['Key'] == tag_name:
            return tag['Value'].replace('"', '')


def get_aws_instances(region):
    try:
        os.environ["AWS_DEFAULT_REGION"] = region
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


def prepare_searchable_instances(aws_regions, instance_data, use_private_ip, use_public_dns_over_ip):
    processed_data = gather_instance_data(aws_regions, instance_data)
    searchable_instances = []

    for instance in processed_data:
        name = get_tag_value('Name', instance['tags'])

        if use_public_dns_over_ip:
            ip = instance['public_dns']
        elif use_private_ip:
            ip = instance['private_ip']
        else:
            ip = instance['public_ip'] or instance['private_ip']

        instance_id = instance.get('instance_id', '')

        if name:
            formatted_instance = '{} ({}){}{}'.format(
                name,
                instance_id,
                SEPARATOR,
                ip
            )
        else:
            formatted_instance = '({}){}{}'.format(
                instance_id,
                SEPARATOR,
                ip
            )
        searchable_instances.append(formatted_instance)

    return searchable_instances
