import os
import sys

SEPARATOR = " @ "
ENV_SSH_USER = os.getenv('AWS_FUZZ_USER')
ENV_KEY_PATH = os.getenv('AWS_FUZZ_KEY_PATH')
ENV_USE_PRIVATE_IP = os.getenv('AWS_FUZZ_PRIVATE_IP')
ENV_SSH_COMMAND_TEMPLATE = os.getenv('AWS_FUZZ_SSH_COMMAND_TEMLPATE', "ssh {user}@{host} -i {key}")

if sys.platform.startswith('linux'):
    lib = 'fzf-0.12.1-linux_386'
elif sys.platform == 'darwin':
    lib = 'fzf-0.12.1-darwin_386'
else:
    print('Currently only MAC OS and Linux are supported, exiting.')
    exit(1)

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