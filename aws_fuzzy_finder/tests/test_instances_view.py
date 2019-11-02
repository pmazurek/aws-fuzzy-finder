from aws_fuzzy_finder.aws_utils import prepare_searchable_instances

aws_default_region = ['us-west-2']

example_reservations = {
    u'us-west-2': {
        u'Reservations': [{
            u'Groups': [],
            u'Instances': [{
                u'PrivateIpAddress': '10.121.111.123',
                u'InstanceId': 'foo-id',
                u'PublicDnsName': 'DNS-foobar',
                u'State': {
                    u'Code': 16,
                    u'Name': 'running'
                },
                u'Tags': [{
                    u'Key': 'Name',
                    u'Value': 'test_foobar"'
                }],
                u'VpcId': 'vpc-f2ccsd34f'
            }, {
                u'PrivateIpAddress': '10.121.12.34',
                u'InstanceId': 'bar-id',
                u'PublicDnsName': 'DNS-prod1',
                u'State': {
                    u'Code': 16,
                    u'Name': 'running'
                },
                u'Tags': [{
                    u'Key': 'Name',
                    u'Value': 'prod_something'
                }],
                u'VpcId': 'vpc-2342sfd2'
            }, {
                u'PrivateIpAddress': '10.121.12.55',
                u'InstanceId': 'baz-id',
                u'PublicIpAddress': '52.123.12.32',
                u'PublicDnsName': 'DNS-prod2',
                u'State': {
                    u'Code': 16,
                    u'Name': 'running'
                },
                u'Tags': [{
                    u'Key': 'Name',
                    u'Value': 'prod_something2'
                }],
                u'VpcId': 'vpc-2342sfd2'
            }]
        }]
    }
}


reservations_with_and_without_name_tags = {
    u'us-west-2': {
        u'Reservations': [{
            u'Groups': [],
            u'Instances': [{
                u'PrivateIpAddress': '10.121.111.123',
                u'InstanceId': 'foo-id',
                u'PublicDnsName': 'DNS-foobar',
                u'State': {
                    u'Code': 16,
                    u'Name': 'running'
                },
                u'Tags': [{
                    u'Key': 'Name',
                    u'Value': 'test_foobar"'
                }],
                u'VpcId': 'vpc-f2ccsd34f'
            }, {
                u'PrivateIpAddress': '10.121.12.34',
                u'InstanceId': 'bar-id',
                u'PublicDnsName': 'DNS-prod1',
                u'State': {
                    u'Code': 16,
                    u'Name': 'running'
                },
                u'Tags': [],
                u'VpcId': 'vpc-2342sfd2'
            }, {
                u'PrivateIpAddress': '10.121.12.55',
                u'InstanceId': 'baz-id',
                u'PublicIpAddress': '52.123.12.32',
                u'PublicDnsName': 'DNS-prod2',
                u'State': {
                    u'Code': 16,
                    u'Name': 'running'
                },
                u'VpcId': 'vpc-2342sfd2'
            }]
        }]
    }
}

aws_fuzz_aws_regions = ['us-west-2', 'us-east-1']
reservations_with_multiple_regions = {
    u'us-west-2': {
        u'Reservations': [{
            u'Groups': [],
            u'Instances': [{
                u'PrivateIpAddress': '10.121.111.123',
                u'InstanceId': 'foo-id-west',
                u'PublicDnsName': 'DNS-foobar',
                u'State': {
                    u'Code': 16,
                    u'Name': 'running'
                },
                u'Tags': [{
                    u'Key': 'Name',
                    u'Value': 'test_foobar_west"'
                }],
                u'VpcId': 'vpc-f2ccsd34f'
            }, {
                u'PrivateIpAddress': '10.121.12.34',
                u'InstanceId': 'bar-id-west',
                u'PublicDnsName': 'DNS-prod1',
                u'State': {
                    u'Code': 16,
                    u'Name': 'running'
                },
                u'Tags': [{
                    u'Key': 'Name',
                    u'Value': 'prod_something_west'
                }],
                u'VpcId': 'vpc-2342sfd2'
            }, {
                u'PrivateIpAddress': '10.121.12.55',
                u'InstanceId': 'baz-id-west',
                u'PublicIpAddress': '52.123.12.32',
                u'PublicDnsName': 'DNS-prod2',
                u'State': {
                    u'Code': 16,
                    u'Name': 'running'
                },
                u'Tags': [{
                    u'Key': 'Name',
                    u'Value': 'prod_something2_west'
                }],
                u'VpcId': 'vpc-2342sfd2'
            }]
        }]
    },
    u'us-east-1': {
        u'Reservations': [{
            u'Groups': [],
            u'Instances': [{
                u'PrivateIpAddress': '10.121.111.124',
                u'InstanceId': 'foo-id-east',
                u'PublicDnsName': 'DNS-foobar',
                u'State': {
                    u'Code': 16,
                    u'Name': 'running'
                },
                u'Tags': [{
                    u'Key': 'Name',
                    u'Value': 'test_foobar_east'
                }],
                u'VpcId': 'vpc-f2ccsd34f'
            }, {
                u'PrivateIpAddress': '10.121.12.35',
                u'InstanceId': 'bar-id-east',
                u'PublicDnsName': 'DNS-prod1',
                u'State': {
                    u'Code': 16,
                    u'Name': 'running'
                },
                u'Tags': [{
                    u'Key': 'Name',
                    u'Value': 'prod_something_east'
                }],
                u'VpcId': 'vpc-2342sfd2'
            }, {
                u'PrivateIpAddress': '10.121.12.77',
                u'InstanceId': 'baz-id-east',
                u'PublicIpAddress': '52.123.12.32',
                u'PublicDnsName': 'DNS-prod2',
                u'State': {
                    u'Code': 16,
                    u'Name': 'running'
                },
                u'Tags': [{
                    u'Key': 'Name',
                    u'Value': 'prod_something2_east'
                }],
                u'VpcId': 'vpc-2342sfd2'
            }]
        }]
    }
}


def test_getting_private_ip():
    searchable_instances = prepare_searchable_instances(
        aws_regions=aws_default_region,
        instance_data=example_reservations,
        use_private_ip=True,
        use_public_dns_over_ip=False,
    )
    assert searchable_instances == [
        'test_foobar (foo-id) @ 10.121.111.123',
        'prod_something (bar-id) @ 10.121.12.34',
        'prod_something2 (baz-id) @ 10.121.12.55',
    ]


def test_getting_public_ip():
    searchable_instances = prepare_searchable_instances(
        aws_regions=aws_default_region,
        instance_data=example_reservations,
        use_private_ip=False,
        use_public_dns_over_ip=False,
    )
    assert searchable_instances == [
        'test_foobar (foo-id) @ 10.121.111.123',
        'prod_something (bar-id) @ 10.121.12.34',
        'prod_something2 (baz-id) @ 52.123.12.32',
    ]


def test_getting_public_dns():
    searchable_instances = prepare_searchable_instances(
        aws_regions=aws_default_region,
        instance_data=example_reservations,
        use_private_ip=False,
        use_public_dns_over_ip=True
    )
    assert searchable_instances == [
        'test_foobar (foo-id) @ DNS-foobar',
        'prod_something (bar-id) @ DNS-prod1',
        'prod_something2 (baz-id) @ DNS-prod2',
    ]


def test_instances_without_name_tag__should_still_be_displayed_with_id_only():
    searchable_instances = prepare_searchable_instances(
        aws_regions=aws_default_region,
        instance_data=reservations_with_and_without_name_tags,
        use_private_ip=False,
        use_public_dns_over_ip=False
    )

    assert searchable_instances == [
        'test_foobar (foo-id) @ 10.121.111.123',
        '(bar-id) @ 10.121.12.34',
        '(baz-id) @ 52.123.12.32',
    ]

def test_getting_instances_from_multiple_regions():
    searchable_instances = prepare_searchable_instances(
    aws_regions=aws_fuzz_aws_regions,
    instance_data=reservations_with_multiple_regions,
    use_private_ip=True,
    use_public_dns_over_ip=False,
    )
    assert searchable_instances == [
        'test_foobar_west (foo-id-west) @ 10.121.111.123',
        'prod_something_west (bar-id-west) @ 10.121.12.34',
        'prod_something2_west (baz-id-west) @ 10.121.12.55',
        'test_foobar_east (foo-id-east) @ 10.121.111.124',
        'prod_something_east (bar-id-east) @ 10.121.12.35',
        'prod_something2_east (baz-id-east) @ 10.121.12.77',
    ]
