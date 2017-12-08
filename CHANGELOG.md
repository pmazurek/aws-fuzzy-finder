# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## [Unreleased]

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

