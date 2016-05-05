# AWS Fuzzy finder

This is a helper app that allows you to ssh into aws instances using fuzzy searching through instances name tags.

![](https://raw.github.com/pmazurek/aws-fuzzy-finder/master/demo.gif)

## Installation

`pip install aws-fuzzy-finder`

Configure your `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY` and `AWS_DEFAULT_REGION` variables as described here: http://boto3.readthedocs.io/en/latest/guide/configuration.html

## Settings

```
Options:
  --private        Use private IP's
  --key-path TEXT  Path to your private key, default: ~/.ssh/id_rsa
  --user TEXT      User to SSH with, default: ec2-user
  --help           Show this message and exit.
```

Or you can append this to your  ~/.bashrc to make the settings permamant:
```
export AWS_FUZZ_USER="your.user"
export AWS_FUZZ_KEY_PATH="~/.ssh/your_private_key"
export AWS_FUZZ_PRIVATE_IP='true' # Delete this one if you want to use public IP's

bind  '"\C-f": "aws-fuzzy\e\C-e\er\C-m"' # This will bind the aws-fuzzy command to ctrl+f
```

`AWS_FUZZ_SSH_COMMAND_TEMLPATE` - set this env var if you want to customize the ssh command , defaults to `ssh {user}@{host} -i {key}`

## Usage

To run, use the following command:

`aws-fuzzy`

To run using a different AWS profile, run the command as follows:

`AWS_DEFAULT_PROFILE=profile_name aws-fuzzy`

Enjoy!
