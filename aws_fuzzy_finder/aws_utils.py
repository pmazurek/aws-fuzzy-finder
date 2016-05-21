import boto3
from botocore.exceptions import NoRegionError, PartialCredentialsError, NoCredentialsError

from .settings import SEPARATOR


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
