from aws_fuzzy_finder.aws_utils import prepare_searchable_instances


example_reservations = [{
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


def test_getting_private_ip():
    searchable_instances = prepare_searchable_instances(
        reservations=example_reservations,
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
        reservations=example_reservations,
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
        reservations=example_reservations,
        use_private_ip=False,
        use_public_dns_over_ip=True
    )
    assert searchable_instances == [
        'test_foobar (foo-id) @ DNS-foobar',
        'prod_something (bar-id) @ DNS-prod1',
        'prod_something2 (baz-id) @ DNS-prod2',
    ]
