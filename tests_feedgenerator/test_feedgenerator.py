# -*- encoding: utf-8 -*-

from __future__ import unicode_literals

try:
    import unittest2 as unittest
except ImportError:
    import unittest

import six
import datetime

import feedgenerator

FIXT_FEED = dict(
    title="Poynter E-Media Tidbits",
    link="http://www.poynter.org/column.asp?id=31",
    description="""A group Weblog by the sharpest minds in online media/journalism/publishing.
    Umlauts: äöüßÄÖÜ
    Chinese: 老师是四十四，是不是？
    Finnish: Mustan kissan paksut posket. (ah, no special chars) Kärpänen sanoi kärpäselle: tuu kattoon kattoon ku kaveri tapettiin tapettiin.
    """,
    language="en"
)
FIXT_ITEM = dict(
    title="Hello",
    link="http://www.holovaty.com/test/",
    description="Testing.",
    content="Full content of our testing entry.",
    pubdate=datetime.datetime(2016,8,11,0,0,0,0),
)


EXPECTED_RESULT_RSS = """<?xml version="1.0" encoding="utf-8"?>
<rss version="2.0"><channel><title>Poynter E-Media Tidbits</title><link>http://www.poynter.org/column.asp?id=31</link><description>A group Weblog by the sharpest minds in online media/journalism/publishing.
    Umlauts: äöüßÄÖÜ
    Chinese: 老师是四十四，是不是？
    Finnish: Mustan kissan paksut posket. (ah, no special chars) Kärpänen sanoi kärpäselle: tuu kattoon kattoon ku kaveri tapettiin tapettiin.
    </description><language>en</language><lastBuildDate>%DATE%</lastBuildDate><item><title>Hello</title><link>http://www.holovaty.com/test/</link><description>Testing.</description><pubDate>Thu, 11 Aug 2016 00:00:00 -0000</pubDate></item></channel></rss>"""

EXPECTED_RESULT_ATOM = """<?xml version="1.0" encoding="utf-8"?>
<feed xml:lang="en" xmlns="http://www.w3.org/2005/Atom"><title>Poynter E-Media Tidbits</title><link href="http://www.poynter.org/column.asp?id=31" rel="alternate"></link><id>http://www.poynter.org/column.asp?id=31</id><updated>%DATE%</updated><subtitle>A group Weblog by the sharpest minds in online media/journalism/publishing.
    Umlauts: äöüßÄÖÜ
    Chinese: 老师是四十四，是不是？
    Finnish: Mustan kissan paksut posket. (ah, no special chars) Kärpänen sanoi kärpäselle: tuu kattoon kattoon ku kaveri tapettiin tapettiin.
    </subtitle><entry><title>Hello</title><link href="http://www.holovaty.com/test/" rel="alternate"></link><published>2016-08-11T00:00:00Z</published><updated>2016-08-11T00:00:00Z</updated><id>tag:www.holovaty.com,2016-08-11:/test/</id><summary type="html">Testing.</summary><content type="html">Full content of our testing entry.</content></entry></feed>"""

ENCODING = 'utf-8'

def build_expected_rss_result(feed, expected_result, encoding):
    # Result's date is of course different from the date in the fixture.
    # So make them equal!
    d = feedgenerator.rfc2822_date(feed.latest_post_date())
    s = expected_result.replace('%DATE%', d)
    if encoding:
        return s.encode(encoding)
    else:
        return s

def build_expected_atom_result(feed, expected_result, encoding):
    # Result's date is of course different from the date in the fixture.
    # So make them equal!
    d = feedgenerator.rfc3339_date(feed.latest_post_date())
    s = expected_result.replace('%DATE%', d)
    if encoding:
        return s.encode(encoding)
    else:
        return s

class TestFeedGenerator(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None

    def test_000_types(self):
        ty = six.text_type
        for k, v in FIXT_FEED.items():
            self.assertEqual(type(v), ty)
        for k, v in FIXT_ITEM.items():
            if k == "pubdate" or k == "updateddate":
                self.assertEqual(type(v), datetime.datetime)
            else:
                self.assertEqual(type(v), ty)
        self.assertEqual(type(EXPECTED_RESULT_RSS), ty)

    def test_001_string_results_rss(self):
        #import ipdb; ipdb.set_trace()
        feed = feedgenerator.Rss201rev2Feed(**FIXT_FEED)
        feed.add_item(**FIXT_ITEM)
        result = feed.writeString(ENCODING)
        if six.PY3:
            # On Python 3, result of feedgenerator is a unicode string!
            # So do not encode our expected_result.
            expected_result = build_expected_rss_result(feed, EXPECTED_RESULT_RSS, None)
        else:
            # On Python 2, result of feedgenerator is a str string!
            # Expected_result must therefore encoded likewise.
            expected_result = build_expected_rss_result(feed, EXPECTED_RESULT_RSS, ENCODING)
        # The different result types of Python 2 (str=bytes) and Python 3
        # (str=text=unicode) stems from a different implementation of StringIO.
        # As I understand it, getvalue() in Python 2 returns the type you
        # originally wrote into the buffer. In Python 3 getvalue() always
        # returns a str (=text=unicode).
        # See other test: test_stringio.py
        #print type(result), type(expected_result)
        self.assertEqual(type(result), type(expected_result))
        self.assertEqual(result, expected_result)

    def test_002_string_results_atom(self):
        #import ipdb; ipdb.set_trace()
        feed = feedgenerator.Atom1Feed(**FIXT_FEED)
        feed.add_item(**FIXT_ITEM)
        result = feed.writeString(ENCODING)
        if six.PY3:
            # On Python 3, result of feedgenerator is a unicode string!
            # So do not encode our expected_result.
            expected_result = build_expected_atom_result(feed, EXPECTED_RESULT_ATOM, None)
        else:
            # On Python 2, result of feedgenerator is a str string!
            # Expected_result must therefore encoded likewise.
            expected_result = build_expected_atom_result(feed, EXPECTED_RESULT_ATOM, ENCODING)
        # The different result types of Python 2 (str=bytes) and Python 3
        # (str=text=unicode) stems from a different implementation of StringIO.
        # As I understand it, getvalue() in Python 2 returns the type you
        # originally wrote into the buffer. In Python 3 getvalue() always
        # returns a str (=text=unicode).
        # See other test: test_stringio.py
        #print type(result), type(expected_result)
        self.assertEqual(type(result), type(expected_result))
        self.assertEqual(result, expected_result)
