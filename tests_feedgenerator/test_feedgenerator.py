import unittest

import datetime

import feedgenerator

import pytest

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
        ty = str
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
        # On Python 3, result of feedgenerator is a unicode string!
        # So do not encode our expected_result.
        expected_result = build_expected_rss_result(feed, EXPECTED_RESULT_RSS, None)
        self.assertEqual(type(result), type(expected_result))
        self.assertEqual(result, expected_result)

    def test_002_string_results_atom(self):
        #import ipdb; ipdb.set_trace()
        feed = feedgenerator.Atom1Feed(**FIXT_FEED)
        feed.add_item(**FIXT_ITEM)
        result = feed.writeString(ENCODING)
        # On Python 3, result of feedgenerator is a unicode string!
        # So do not encode our expected_result.
        expected_result = build_expected_atom_result(feed, EXPECTED_RESULT_ATOM, None)
        self.assertEqual(type(result), type(expected_result))
        self.assertEqual(result, expected_result)


@pytest.mark.parametrize("description, subtitle, fragment, nonfragment", [
    # Neither description nor subtitle are provided
    (None, None, None, "<subtitle></subtitle>"),
    ("", "", None, "<subtitle></subtitle>"),
    # Description is provided
    ("description", None, "<subtitle>description</subtitle>", None),
    ("description", "", "<subtitle>description</subtitle>", None),
    # Subtitle is provided
    (None, "subtitle", "<subtitle>subtitle</subtitle>", None),
    ("", "subtitle", "<subtitle>subtitle</subtitle>", None),
    # Both description & subtitle are provided; subtitle takes precedence
    ("description", "subtitle", "<subtitle>subtitle</subtitle>", "<subtitle>description</subtitle>"),
])
def test_subtitle(description, subtitle, fragment, nonfragment):
    """Test regression for https://github.com/getpelican/feedgenerator/issues/30.

    We test against all four possible combinations of description x
    subtitle parameters and additionally for None and "".

    description, subtitle are the values for the respective
    feed-parameters.

    fragment and nonfragment are text fragments that should be in the
    expected result or not.

    """
    FIXT_FEED = dict(
        title="title",
        link="https://example.com",
        description=description,
        subtitle=subtitle,
    )
    feed = feedgenerator.Atom1Feed(**FIXT_FEED)
    result = feed.writeString(ENCODING)
    if fragment:
        assert fragment in result
    if nonfragment:
        assert nonfragment not in result
