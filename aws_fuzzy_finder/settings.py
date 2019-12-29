import os
import sys

from os.path import expanduser

SEPARATOR = " @ "
ENV_SSH_USER = os.getenv('AWS_FUZZ_USER')
ENV_KEY_PATH = os.getenv('AWS_FUZZ_KEY_PATH')
ENV_USE_PRIVATE_IP = os.getenv('AWS_FUZZ_PRIVATE_IP')
ENV_USE_PUBLIC_DNS_OVER_IP = os.getenv('AWS_FUZZ_DNS_OVER_IP', False)  # use public DNS over IP (both public or private)
ENV_TUNNEL_SSH_USER = os.getenv('AWS_FUZZ_TUNNEL_USER')
ENV_TUNNEL_KEY_PATH = os.getenv('AWS_FUZZ_TUNNEL_KEY_PATH')
ENV_SSH_COMMAND_TEMPLATE = os.getenv('AWS_FUZZ_SSH_COMMAND_TEMPLATE', "ssh {key} {user}{host}")
ENV_AWS_REGIONS = os.getenv('AWS_FUZZ_AWS_REGIONS', '')
CACHE_EXPIRY_TIME = int(os.getenv('AWS_FUZZ_CACHE_EXPIRY', 3600))
CACHE_ENABLED = os.getenv('AWS_FUZZ_USE_CACHE', False)
AWS_DEFAULT_PROFILE=os.getenv('AWS_DEFAULT_PROFILE', 'default')
CACHE_DIR = '{}/{}'.format(expanduser("~"), '.aws_fuzzy_finder_cache')
CACHE_PATH = '{}/{}'.format(CACHE_DIR, AWS_DEFAULT_PROFILE)

fzf_base = 'fzf-0.17.0'
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

if ENV_AWS_REGIONS:
    regions = ENV_AWS_REGIONS.split(",")
else:
    regions = [os.getenv("AWS_DEFAULT_REGION")]
AWS_REGIONS = regions

NO_REGION_ERROR = """No AWS region specified.
Specify region in your boto config or add a "AWS_DEFAULT_REGION" environment variable.
$ export AWS_DEFAULT_REGION="<your_region_code>"
For more info visit:
http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-regions-availability-zones.html#concepts-available-regions"""

NO_CREDENTIALS_ERROR = """No AWS credentials specified.
Make sure to set your aws_access_key_id, aws_secret_access_key and region in your boto config
as described here: http://boto3.readthedocs.io/en/latest/guide/configuration.html"""

WRONG_CREDENTIALS_ERROR = "Authentication failure, check your AWS credentials"
