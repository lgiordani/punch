=======
History
=======

2.0.0 (2019-11-07)
------------------

* **DEPRECATION** Punch doesn't support `GLOBAL` variables in the `FILES` variable anymore. The values given to fields in the `FILES` section are now simple strings and are not processed through Jinja2 anymore.
* Initial drop of Python 2.x: the CI process doesn't test Python2.x anymore.
* Complete review of documentation: the docs have been split in multiple files to make it easier to find information and to understand the program.
* Initial implementation of automatic documentation from tests. Integration tests can now be parsed to extract examples for the documentation. [See documentation: `Examples from tests`]
* Named serializers: serializers now can be given a name through a dictionary syntax. With this change it becomes possible to select the serializer to use for the VCS. [See documentation: `Configuration > GLOBALS`]
* Complex serializers: standard serializers use the same pattern both for the search and for the replace actions. With complex serializers you can define two different patterns, one for each action. [See documentation: `Advanced configuration > Complex serializers`]
* The configuration of each file managed by Punch can override the global serializers or add new ones. [See documentation: `Configuration > FILES`]
* Release notes: Punch can be configured to check if a pattern based on the new version is present in the managed files. This makes it simple to check if HISTORY files have been updated without requiring to interrupt the execution of the program and later restore it. [See documentation: `Advanced configuration > Release notes`]


1.6.2 (2019-08-22)
------------------

* Updating the HISTORY file and considering that it is high time I come up with a solution
  for files that require manual intervention when updating the version.

1.6.1 (2019-08-22)
------------------

* Merged PR#38: Fixes the behaviour of the standard annotation message

1.6.0 (2019-04-12)
------------------

* Merged PR #37: Adds a --quiet option to suppress all warnings
* Added VCS information to --simulate
* Tests updated to use latest pytest features and to remove deprecated features
* Fixed the requirements setup (development.txt now inherits testing.txt)
* Internal structure improvements to ease the development of new features like enhanced actions

1.5.0 (2018-05-03)
------------------

* Fixed issue #31: Punch doesn't add files to commits + make file additions configurable
* Fixed part of issue #34: [git VCS] Additional branch options (by joshua-s)
* Added 'include_files' and 'include_all_files' flags (issue #31)
* Added 'target_branch' flag (issue #34)

1.4.5 (2018-04-20)
------------------

* Using version.to_file in CLI (PR#33 by gthank)

1.4.4 (2018-04-18)
------------------

* Fixed wrong behaviour of DateVersionPart (PR#32 by gthank)

1.4.3 (2018-03-21)
------------------

* Fixed issue #23: Print a warning when no match is found in controlled files
* Fixed issue #27: Possible typo in docs
* Fixed issue #29: punch silently adds and commits unrelated untracked files to git

1.4.2 (2017-10-05)
------------------

* Fixed error with months and days ending with 0

1.4.1 (2017-09-16)
------------------

* Minor fixes to the date part representation

1.4.0 (2017-06-07)
------------------

* Support for actions to specify complex behaviours
* PEP8 compliance global review

1.3.2 (2017-03-29)
------------------

* Fixed CLI script installation on Windows (by jobec)

1.3.1 (2017-01-23)
------------------

* Readthedocs documentation link added to README

1.3.0 (2017-01-20)
------------------

* Date-base version part added (with support for CalVer syntax)

1.2.0 (2016-09-09)
------------------

* Mercurial support added by Michele D'Amico

1.1.2 (2016-06-09)
------------------

* Fixed issue #7

1.1.1 (2016-06-01)
------------------

* Fixed issues #3, #4, #5

1.1.0 (2016-05-26)
------------------

* Added --set-part and --reset-on-set flags

1.0.2 (2016-05-24)
------------------

* Fixed the PyPI badge in the documentation
* Added some examples both in documentation and in the test suite

1.0.1 (2016-05-21)
------------------

* Last minute change of package name on PyPI due to a name clash.

1.0.0 (2016-05-19)
------------------

* First release on PyPI.
