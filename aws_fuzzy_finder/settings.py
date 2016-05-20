import os
import sys

from os.path import expanduser

SEPARATOR = " @ "
ENV_SSH_USER = os.getenv('AWS_FUZZ_USER')
ENV_KEY_PATH = os.getenv('AWS_FUZZ_KEY_PATH')
ENV_USE_PRIVATE_IP = os.getenv('AWS_FUZZ_PRIVATE_IP')
ENV_TUNNEL_SSH_USER = os.getenv('AWS_FUZZ_TUNNEL_USER')
ENV_TUNNEL_KEY_PATH = os.getenv('AWS_FUZZ_TUNNEL_KEY_PATH')
ENV_USE_PRIVATE_IP = os.getenv('AWS_FUZZ_PRIVATE_IP')
ENV_SSH_COMMAND_TEMPLATE = os.getenv('AWS_FUZZ_SSH_COMMAND_TEMLPATE', "ssh -i {key} {user}@{host}")
CACHE_EXPIRY_TIME = os.getenv('AWS_FUZZ_CACHE_EXPIRY', 60)
CACHE_ENABLED = os.getenv('AWS_FUZZ_USE_CACHE', True)
CACHE_PATH = '{}/{}'.format(
    expanduser("~"),
    '.aws_fuzzy_finder.cache'
)

fzf_base = 'fzf-0.12.1'
is_64_bit = sys.maxsize > 2**32

if is_64_bit:
    arch = 'amd64'
else:
    arch = '386'

if sys.platform.startswith('linux'):
    system = 'linux'
elif sys.platform == 'darwin':
    system = 'darwin'
else:
    print('Currently only MAC OS and Linux are supported, exiting.')
    exit(1)

lib = '{}-{}_{}'.format(fzf_base, system, arch)

LIBRARY_PATH = '{}/libs/{}'.format(
    os.path.dirname(os.path.abspath(__file__)),
    lib
)

NO_REGION_ERROR = """No AWS region specified.
Specify region in your boto config or add a "AWS_DEFAULT_REGION" environment variable.
$ export AWS_DEFAULT_REGION="<your_region_code>"
For more info visit:
http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-regions-availability-zones.html#concepts-available-regions"""

NO_CREDENTIALS_ERROR = """No AWS credentials specified.
Make sure to set your aws_access_key_id, aws_secret_access_key and region in your boto config
as described here: http://boto3.readthedocs.io/en/latest/guide/configuration.html"""

WRONG_CREDENTIALS_ERROR = "Authentication failure, check your AWS credentials"
