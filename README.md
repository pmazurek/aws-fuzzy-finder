[![Build Status](https://travis-ci.org/pmazurek/aws-fuzzy-finder.svg?branch=master)](https://travis-ci.org/pmazurek/aws-fuzzy-finder)

# AWS Fuzzy Finder

`aws-fuzzy-finder` aims at one thing: making the process of finding the IPs and SSH'ing into your EC2 instances super fast and easy. It will connect with AWS, automatically grab all the instances you have access to, and present them to you in a fuzzy searchable way!

![](https://raw.github.com/pmazurek/aws-fuzzy-finder/master/demo.gif)

It is built on top of [fzf](https://github.com/junegunn/fzf-bin/releases) binaries and [boto3](https://github.com/boto/boto3).


## Installation

To install use the following command:

`pip install aws-fuzzy-finder`

#### Manual install steps:

1. Clone the repo
2. In the repo directory run `python setup.py install`

This package uses `boto` to authenticate, so if you have your `aws-cli` or `ansible`
configured and working, you can skip the following step, it will work out of the box.

if not, create `~/.aws/credentials` file and make it look like this:

```
[default]
aws_access_key_id = your_key
aws_secret_access_key = your_secret
region = your_region_code
```

More information on alternative ways of configuring your `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY` and `AWS_DEFAULT_REGION` variables can be found here: http://boto3.readthedocs.io/en/latest/guide/configuration.html

## Settings

You will need to set the user you want to SSH with and the path to your ssh key. `--ssh-user` will default to `ec2-user` and `--key-path` will default to `~/.ssh/id_rsa` so if you use defaults, you can skip this step.

If you want to use private IP's instead of public ones, use `--private` flag.

Either use the command line params, or you can append this to your  `~/.bashrc` to make the settings permamant:
```
export AWS_FUZZ_USER="your.user"
export AWS_FUZZ_KEY_PATH="~/.ssh/your_private_key"
export AWS_FUZZ_PRIVATE_IP='true' # Delete this one if you want to use public IP's
```
Remeber that every change to `~/.bashrc` requires you to re-load it: `source ~/.bashrc` or restart terminal.

`AWS_FUZZ_SSH_COMMAND_TEMPLATE` - set this env var if you want to customize the ssh command , defaults to `ssh {key} {user}{host}`

## Multiple Regions
Getting instances from multiple regions instead of just one.
If you have a large amount of instances adding more regions will significantly slow down the initial collection of data before it is presented to you on the screen.

This is optional, aws-fuzzy will use the `AWS_DEFAULT_REGION` by default and using the multiple regions option will ignore this.

In your `~/.bashrc` append a list of AWS Regions separated by a comma and nothing else. The lists minimum size is one and has no maximum.

`AWS_FUZZ_REGIONS="us-west-2,us-east-1,eu-central-1,ap-southeast-2,ap-northeast-1"`

List of AWS Regions can be found here: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-regions-availability-zones.html#concepts-available-regions

## Usage

To run, use the following command:

`aws-fuzzy`

To run using a different AWS profile, run the command as follows:

`AWS_DEFAULT_PROFILE=profile_name aws-fuzzy`

Enjoy!

## Key bindings
It is very convenient to bind various aws-fuzzy profiles/settings to keys. This gives you even faster access to your instances. To achieve this, add this to your `~/.bashrc`:

```
# This will bind the aws-fuzzy command to ctrl+f
bind  '"\C-f": "aws-fuzzy\e\C-e\er\C-m"'

# You can bind different settings to different keys
bind  '"\C-a": "AWS_DEFAULT_PROFILE=production aws-fuzzy --private\e\C-e\er\C-m"'
```


## Advanced usage
Sometimes you need to use only the IP of the instance. You can use this command to interactively pick IP's to use with other commands.
To do so, add `--ip-only` as a parameter. Example usage:

```
$ echo "foo $(aws-fuzzy --ip-only) bar"
> foo 10.123.42.12 bar
```

Example to make ansible interactive:
```
$ ansible --become --ask-become-pass -v -i "$(aws-fuzzy --ip-only)," all -m shell -a "setenforce 0"
```

This will bring an interactive prompt, and the IP of the instance of your choice will
be used. You can combine it with basically any command you want, sky is the limit now ;)

## Cache

If you are managing lots of instances and downloading the data takes too long, you can use the built in cache. To enable it set the following variables in your `.bashrc`:
```
export AWS_FUZZ_USE_CACHE=yes
export AWS_FUZZ_CACHE_EXPIRY=3600  # expiry time in seconds
```

If you set `AWS_FUZZ_CACHE_EXPIRY=0` to zero, it will never expire your cache.
To invalidate cache and refresh data, run with `--no-cache` param.
Cache will be stored as a file in `~/.aws_fuzzy_finder_cache/` directory per AWS profile.

## Tunneling

If you have to access your instances through a gateway instance, use the `--tunneling` param. This will make the fuzzy find to run twice: first time you will pick the gateway to tunnel through, and the second time you choose is the instance you would like to SSH into.

Gateway must be allowed to access the instance with its own ssh key. You may set the user and key path spearately using `--tunnel-user` and `--tunnel-key-path` params. The key will be looked up ON the gateway instace.

## Dependency conflicts/ Virtualenvs

It's 2018, Summer and you are using `pip` to install `aws-fuzzy-finder` along with `awscli` on the same machine, but it fails, you see errors about botocore, you become sad.
You want to be able to use both tools in a convenient and easy way. You accept that some initial configuration is OK, and a happy life afterwards is great, you are no longer sad.

Firstly we will need, python setup tools and virtualenv as provided by your distribution. (I assume you are using a Linux).

We will modify our pip config, so that packages installed with pip are always installed locally to / for the user, because you probably will not be running aws-fuzzy-finder as a system service.


Create a file in your home >> .config >> pip directory:

```
~/.config/pip/pip.conf
```

add this to the file

```
[install]
user = yes
no-binary = :all:
```

Then we will create a directory where we will store all the virtual environments for all tools that we might want to install like this.

```
mkdir -p ~/.virtualenvs
```

Now let's install awscli:

```
cd ~/.virtualenvs
virtualenv --system-site-packages -p python3 awscli
. awscli/bin/activate
pip install awscli
deactivate
```

Now let's install aws-fuzzy-finder:

```
cd ~/.virtualenvs
virtualenv --system-site-packages -p python3 aws-fuzzy-finder
. aws-fuzzy-finder/bin/activate
pip install aws-fuzzy-finder
deactivate
```

Now, in your `~/.local/bin/` directory, you should see `aws` "binary" and a `aws-fuzzy` "binary".
If you `head -n1 ~/.local/bin/aws` you should see something like:
```
#!/home/your-user-name/.virtualenvs/awscli/bin/python
```
This is essentially telling the "binary" to use the virtual environment we specifically created just for this tool.

No more conflicts!!!
