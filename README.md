# AWS Fuzzy finder

This is a helper app that allows you to ssh into aws instances using fuzzy searching through instances name tags.

[![asciicast](https://asciinema.org/a/1fzqrev6rn1mp9e68i4e9ri7g.png)](https://asciinema.org/a/1fzqrev6rn1mp9e68i4e9ri7g)


## Installation

This package _heavily_ depends on fzf: https://github.com/junegunn/fzf

To install fzf, do:
```
git clone --depth 1 https://github.com/junegunn/fzf.git ~/.fzf
~/.fzf/install
```

To install the package itself, do:
`pip install aws-fuzzy-finder`
or install for development
```
git clone git@github.com:pmazurek/aws-fuzzy-finder.git
cd aws-fuzzy-finder && pip install -e .
```

## Settings

Add the following environment variables to your .bashrc:

- `AWS_FUZZ_USER` - default user to use with SSH command
- `AWS_FUZZ_KEY_PATH` - path to your private key with which you are authorised on the instances


## Usage

To run, use the following command:

`aws-fuzzy`

Enjoy!
