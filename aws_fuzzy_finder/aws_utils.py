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
