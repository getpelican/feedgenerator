CHANGELOG
=========

2.2.0 - 2025-07-14
------------------

- Update to latest upstream code from Django 5.2
- Remove `pytz` as a dependency on non-Windows systems
- Use standardized `pyproject` file
- Drop support for EOL Python 3.7 & 3.8

2.1.0 - 2023-04-14
------------------

* Modernize and improve tests ([#32](https://github.com/getpelican/feedgenerator/pull/32) & [#34](https://github.com/getpelican/feedgenerator/pull/34) — thanks to @venthur)
* Drop support for Python 3.6 and test on 3.10 & 3.11 ([#35](https://github.com/getpelican/feedgenerator/pull/35) — thanks to @hugovk)
* Exclude `tests_feedgenerator/__pycache__` from distribution ([#33](https://github.com/getpelican/feedgenerator/pull/33) — thanks to @BenSturmfels)

2.0.0 - 2021-09-28
------------------

* Add preliminary support for adding images to feeds
* Update code for Python 3.6+
* Drop support for Python 2.7
* Fix double subtitles if both description & subtitle are provided

1.9.2 - 2021-08-18
------------------

Use description field as subtitle for Atom feeds, if provided

1.9.1 - 2020-02-09
------------------

Trim files included in source tarball

1.9.0 - 2016-09-12
------------------

* Always set the `updated` element of an `entry` in Atom feeds
* Change `get_tag_uri()` so the `/` before a fragment gets only added if there is a fragment

1.8.0 - 2016-04-05
------------------

* Support Atom’s `<content>` element
* Put Atom pubdate in `<published>`, not `<updated>`
* Support giving an explicit `<updated>` for Atom

1.7.0 - 2013-08-31
------------------

Set minimum pytz version

1.6.0 - 2013-06-02
------------------

Add Python 3 support

1.5.0 - 2013-01-11
------------------

Added tests

1.2.1 - 2010-08-19
------------------

Initial packaged release
