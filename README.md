# AWS Fuzzy Finder

`aws-fuzzy-finder` aims at one thing: making the process of finding the IPs and SSH'ing into your EC2 instances super fast and easy.

![](https://raw.github.com/pmazurek/aws-fuzzy-finder/master/demo.gif)

It is built on top of [fzf](https://github.com/junegunn/fzf-bin/releases) binaries and [boto3](https://github.com/boto/boto3).

## Important

This package is very young and is not yet widely used and didn't go through a lot of testing.
If you find a bug, make sure to open an issue. If you can think of a way to improve it, open an issue and let me know.
If you like it and feel like your workflow benefits from it, make sure to contribute towards its popularity somehow.
Share it, post it somewhere, star it, tell your friends, tell your colleagues. Thanks!

## Installation

To install use the following command:

`pip install aws-fuzzy-finder`

This package uses `boto` to authenticate, so if you have your `aws-cli`, `ansible` or `boto` 
configured and working, you can skip the following step, it will work out of the box.

if not, create `~/.aws/credentials` file and make it look like this:

```
[default]
aws_access_key_id = <your_key>
aws_secret_access_key = <your_secret>
region = <your_region_code>
```

More information on alternative ways of configuring your `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY` and `AWS_DEFAULT_REGION` variables can be found here: http://boto3.readthedocs.io/en/latest/guide/configuration.html

## Settings

```
Options:
  --private        Use private IP's
  --key-path TEXT  Path to your private key, default: ~/.ssh/id_rsa
  --user TEXT      User to SSH with, default: ec2-user
  --ip-only        Print chosen IP to STDOUT and exit
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

## Advanced usage
Sometimes you need to use only the IP of the instance. You can use this command to interactively pick IP's to use with other commands.
To do so, add `--ip-only` as a parameter. Example usage:

```
$ echo "foo $(aws-fuzzy --ip-only) bar"
> foo 10.123.42.12 bar
```

Example to make ansible interactive:
```
$ ansible --become --ask-become-pass -v -i "$(aws-fuzzy --ip-only)" all -m shell -a "setenforce 0"
```

This will bring an interactive prompt, and the IP of the instance of your choice will
be used. You can combine it with basically any command you want, sky is the limit now ;)
