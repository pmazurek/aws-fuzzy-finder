# AWS Fuzzy finder

This is a helper app that allows you to ssh into aws instances using fuzzy searching through instances name tags.

![](https://raw.github.com/pmazurek/aws-fuzzy-finder/master/demo.gif)

## Installation

`pip install aws-fuzzy-finder`

This package _heavily_ depends on fzf: https://github.com/junegunn/fzf

To install fzf, do:
```
git clone --depth 1 https://github.com/junegunn/fzf.git ~/.fzf
~/.fzf/install
```

## Settings

Add the following environment variables to your .bashrc:

- `AWS_FUZZ_USER` - default user to use with SSH command - defaults to `ec2-user`
- `AWS_FUZZ_KEY_PATH` - path to your private key with which you are authorised on the instances - defaults to `~/.ssh/id_rsa`

### Important !!
Make sure you have your `AWS_ACCESS_KEY_ID` `AWS_SECRET_ACCESS_KEY` and `AWS_DEFAULT_REGION` configured as per http://boto3.readthedocs.io/en/latest/guide/configuration.html


## Usage

To run, use the following command:

`aws-fuzzy`

This app will use your default `AWS_PROFILE` to query AWS api for all the instances details.

Enjoy!

## TODO
- Add a env variable to allow for switching between either public or private IP (currently app defaults to use only private IP's)
- Add keybinding to bash (eg. alt+s) to make it even easier to use
- Add install script that will install fzf, add all the env vars to bashrc and configure keybindings
- Stop depending on `fzf`, because its not in pip, which complicates installation :(
