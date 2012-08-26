# -*- encoding: utf-8 -*-

from __future__ import unicode_literals

import re
try:
    import unittest2 as unittest
except ImportError:
    import unittest

import six

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
    description="Testing."
)

FIXT_FEED_BYTES = dict(
    title=six.b("Poynter E-Media Tidbits"),
    link=six.b("http://www.poynter.org/column.asp?id=31"),
    description=six.b("""A group Weblog by the sharpest minds in online media/journalism/publishing.
    Umlauts: äöüßÄÖÜ
    Chinese: 老师是四十四，是不是？
    Finnish: Mustan kissan paksut posket. (ah, no special chars) Kärpänen sanoi kärpäselle: tuu kattoon kattoon ku kaveri tapettiin tapettiin.
    """),
    language=six.b("en")
)
FIXT_ITEM_BYTES = dict(
    title=six.b("Hello"),
    link=six.b("http://www.holovaty.com/test/"),
    description=six.b("Testing.")
)

EXPECTED_RESULT = """<?xml version="1.0" encoding="utf-8"?>
<rss xmlns:atom="http://www.w3.org/2005/Atom" version="2.0"><channel><title>Poynter E-Media Tidbits</title><link>http://www.poynter.org/column.asp?id=31</link><description>A group Weblog by the sharpest minds in online media/journalism/publishing.
    Umlauts: äöüßÄÖÜ
    Chinese: 老师是四十四，是不是？
    Finnish: Mustan kissan paksut posket. (ah, no special chars) Kärpänen sanoi kärpäselle: tuu kattoon kattoon ku kaveri tapettiin tapettiin.
    </description><language>en</language><lastBuildDate>Sun, 26 Aug 2012 07:44:28 -0000</lastBuildDate><item><title>Hello</title><link>http://www.holovaty.com/test/</link><description>Testing.</description></item></channel></rss>"""

EXPECTED_RESULT_BYTES = six.b("""<?xml version="1.0" encoding="utf-8"?>
<rss xmlns:atom="http://www.w3.org/2005/Atom" version="2.0"><channel><title>Poynter E-Media Tidbits</title><link>http://www.poynter.org/column.asp?id=31</link><description>A group Weblog by the sharpest minds in online media/journalism/publishing.
    Umlauts: äöüßÄÖÜ
    Chinese: 老师是四十四，是不是？
    Finnish: Mustan kissan paksut posket. (ah, no special chars) Kärpänen sanoi kärpäselle: tuu kattoon kattoon ku kaveri tapettiin tapettiin.
    </description><language>en</language><lastBuildDate>Sun, 26 Aug 2012 07:44:28 -0000</lastBuildDate><item><title>Hello</title><link>http://www.holovaty.com/test/</link><description>Testing.</description></item></channel></rss>""")

RE_BUILD_DATE = re.compile('<lastBuildDate>.*?</lastBuildDate>')

ENCODING = 'utf-8'


def build_expected_result(feed, expected_result, encoding):
    d = feedgenerator.rfc2822_date(feed.latest_post_date())
    return RE_BUILD_DATE.sub('<lastBuildDate>'+d+'</lastBuildDate>',
        expected_result).encode(encoding)


class TestFeedGenerator(unittest.TestCase):

    def test_001_default_encoding(self):
        # Default encoding is unicode since we have imported unicode_literals!
        feed = feedgenerator.Rss201rev2Feed(**FIXT_FEED)
        feed.add_item(**FIXT_ITEM)
        result = feed.writeString(ENCODING)
        expected_result = build_expected_result(feed, EXPECTED_RESULT, ENCODING)
        self.assertEqual(result, expected_result)

    def test_002_bytes(self):
        feed = feedgenerator.Rss201rev2Feed(**FIXT_FEED_BYTES)
        feed.add_item(**FIXT_ITEM_BYTES)
        result = feed.writeString(ENCODING)
        expected_result = build_expected_result(feed, EXPECTED_RESULT_BYTES, ENCODING)
        self.assertEqual(result, expected_result)
