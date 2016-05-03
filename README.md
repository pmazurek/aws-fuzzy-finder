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

Or you can add following environment variables to your .bashrc to make the settings permamant:

- `AWS_FUZZ_USER` - default user to use with SSH command - defaults to `ec2-user`
- `AWS_FUZZ_KEY_PATH` - path to your private key with which you are authorised on the instances - defaults to `~/.ssh/id_rsa`
- `AWS_FUZZ_PRIVATE_IP` - set if you want to use only private IP's to connect to instances
- `AWS_FUZZ_SSH_COMMAND_TEMLPATE` - set if you want to customize the ssh command , defaults to `ssh {user}@{host} -i {key}`


## Usage

To run, use the following command:

`aws-fuzzy`

This app will use your default `AWS_PROFILE` to query AWS api for all the instances details.

Enjoy!

## TODO
- Add keybinding to bash (eg. alt+s) to make it even easier to use
- Add install script that will install fzf, add all the env vars to bashrc and configure keybindings
