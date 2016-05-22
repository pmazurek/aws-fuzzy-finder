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
