# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.1.1] - 2021-02-24

### Added

+ [#40][p40] Adding support for aws SSM by @jwhaley-togetherwork

### Changed

+ [#39][p39] Fix for cache behaviour by @AndreZiviani

[p40]: https://github.com/pmazurek/aws-fuzzy-finder/pull/40
[p39]: https://github.com/pmazurek/aws-fuzzy-finder/pull/39

## [1.1.0] - 2019-12-29

### Added
+ [#36][p36] Added support for multiple AWS regions by @sergekh42

### Changed

+ [#33][p33] Creates a different cache for each aws profile by @joaogbcravo
+ [#36][p36] Removed deprecated `boto3-session-cache` by @sergekh42
+ [#37][p37] We no longer run test this package on TravisCI with Python versions that effectively reached EOL (2.7, 3.4).
  However we added 3.7 (stable) and 3.8.

[p33]: https://github.com/pmazurek/aws-fuzzy-finder/pull/33
[p36]: https://github.com/pmazurek/aws-fuzzy-finder/pull/36
[p37]: https://github.com/pmazurek/aws-fuzzy-finder/pull/37

## [1.0.0] - 2018-11-21

### Added

+ [#32][p32] Added Boto3 Session Cache by @joaogbcravo

[p32]: https://github.com/pmazurek/aws-fuzzy-finder/pull/32

## [0.3.6] - 2017-12-08

### Added

+ [#15][p15] & [#16][p16]- Add PublicDNS support by @Twista

[p16]: https://github.com/pmazurek/aws-fuzzy-finder/pull/16
[p15]: https://github.com/pmazurek/aws-fuzzy-finder/pull/15

### Fixed

+ [#27][p27] - Fixed `setup.py` to reference correct binary deps by @khornberg
+ [#23][p23] - `PublicDnsName` is optional & fixed invocation of `prepare_searchable_instances`
+ [#17][p17] - Fix typos in env variable names by @flou

[p27]: https://github.com/pmazurek/aws-fuzzy-finder/pull/27
[p23]: https://github.com/pmazurek/aws-fuzzy-finder/pull/23
[p17]: https://github.com/pmazurek/aws-fuzzy-finder/pull/17

### Changed

+ [#25][p25] - Upgraded fzf libs to v0.17.0

[p25]: https://github.com/pmazurek/aws-fuzzy-finder/pull/25

# 0.3.5
+ Adding tunneling
+ Adding file based cache

# 0.3.4
+ Adding full 32/64 bit support, issue #7

# 0.3.3
+ Adding `--ip-only` functionality

# 0.3.2
+ Bugfix, fixing linux platform detection, issue #3

# 0.3.1
+ Bugfix, adding correct mac package

# 0.3
+ Adding mac support

# 0.2.1
+ Embeding fzf into package

# 0.2
+ Adding `click` as command line arg parser, adding public ip support

