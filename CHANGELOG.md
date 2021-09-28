CHANGELOG
=========

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
