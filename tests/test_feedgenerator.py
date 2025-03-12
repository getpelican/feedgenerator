import datetime
from zoneinfo import ZoneInfo

import pytest

import feedgenerator

AWARE_DATE = datetime.datetime(2016,8,11,0,0,0,0,tzinfo=ZoneInfo("America/New_York"))
AWARE_DATE_UTC = datetime.datetime(2016,8,11,0,0,0,0,tzinfo=ZoneInfo("UTC"))
NAIVE_DATE = datetime.datetime(2016,8,11,0,0,0,0)

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
    link="http://www.holovaty.com/täst/",
    description="Testing.",
    content="Full content of our testing entry.",
    pubdate=NAIVE_DATE,
)


EXPECTED_RESULT_RSS = """<?xml version="1.0" encoding="utf-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom"><channel><title>Poynter E-Media Tidbits</title><link>http://www.poynter.org/column.asp?id=31</link><description>A group Weblog by the sharpest minds in online media/journalism/publishing.
    Umlauts: äöüßÄÖÜ
    Chinese: 老师是四十四，是不是？
    Finnish: Mustan kissan paksut posket. (ah, no special chars) Kärpänen sanoi kärpäselle: tuu kattoon kattoon ku kaveri tapettiin tapettiin.
    </description><language>en</language><lastBuildDate>%DATE%</lastBuildDate><item><title>Hello</title><link>http://www.holovaty.com/t%C3%A4st/</link><description>Testing.</description><pubDate>Thu, 11 Aug 2016 00:00:00 -0000</pubDate></item></channel></rss>"""

EXPECTED_RESULT_ATOM = """<?xml version="1.0" encoding="utf-8"?>
<feed xml:lang="en" xmlns="http://www.w3.org/2005/Atom"><title>Poynter E-Media Tidbits</title><link href="http://www.poynter.org/column.asp?id=31" rel="alternate"/><id>http://www.poynter.org/column.asp?id=31</id><updated>%DATE%</updated><subtitle>A group Weblog by the sharpest minds in online media/journalism/publishing.
    Umlauts: äöüßÄÖÜ
    Chinese: 老师是四十四，是不是？
    Finnish: Mustan kissan paksut posket. (ah, no special chars) Kärpänen sanoi kärpäselle: tuu kattoon kattoon ku kaveri tapettiin tapettiin.
    </subtitle><entry><title>Hello</title><link href="http://www.holovaty.com/t%C3%A4st/" rel="alternate"/><published>2016-08-11T00:00:00Z</published><updated>2016-08-11T00:00:00Z</updated><id>tag:www.holovaty.com,2016-08-11:/t%C3%A4st/</id><summary type="html">Testing.</summary><content type="html">Full content of our testing entry.</content></entry></feed>"""

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


def test_000_types():
    for k, v in FIXT_FEED.items():
        assert isinstance(v, str)
    for k, v in FIXT_ITEM.items():
        if k == "pubdate" or k == "updateddate":
            assert isinstance(v, datetime.datetime)
        else:
            assert isinstance(v, str)
    assert isinstance(EXPECTED_RESULT_RSS, str)


def test_001_string_results_rss():
    #import ipdb; ipdb.set_trace()
    feed = feedgenerator.Rss201rev2Feed(**FIXT_FEED)
    feed.add_item(**FIXT_ITEM)
    result = feed.writeString(ENCODING)
    # On Python 3, result of feedgenerator is a unicode string!
    # So do not encode our expected_result.
    expected_result = build_expected_rss_result(feed, EXPECTED_RESULT_RSS, None)
    assert isinstance(result, type(expected_result))
    assert result == expected_result


def test_002_string_results_atom():
    #import ipdb; ipdb.set_trace()
    feed = feedgenerator.Atom1Feed(**FIXT_FEED)
    feed.add_item(**FIXT_ITEM)
    result = feed.writeString(ENCODING)
    # On Python 3, result of feedgenerator is a unicode string!
    # So do not encode our expected_result.
    expected_result = build_expected_atom_result(feed, EXPECTED_RESULT_ATOM, None)
    assert isinstance(result, type(expected_result))
    assert result == expected_result


@pytest.mark.parametrize("description, subtitle, fragment, nonfragment", [
    # Neither description nor subtitle are provided
    (None, None, None, "<subtitle/>"),
    ("", "", None, "<subtitle/>"),
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

@pytest.mark.parametrize("generator, date, expected_date_string", [
    (feedgenerator.Atom1Feed, AWARE_DATE, "2016-08-11T00:00:00-04:00"),
    (feedgenerator.Atom1Feed, AWARE_DATE_UTC, "2016-08-11T00:00:00+00:00"),
    (feedgenerator.Atom1Feed, NAIVE_DATE, "2016-08-11T00:00:00Z"),
    (feedgenerator.Rss201rev2Feed, AWARE_DATE, "Thu, 11 Aug 2016 00:00:00 -0400"),
    (feedgenerator.Rss201rev2Feed, AWARE_DATE_UTC, "Thu, 11 Aug 2016 00:00:00 +0000"),
    (feedgenerator.Rss201rev2Feed, NAIVE_DATE, "Thu, 11 Aug 2016 00:00:00 -0000"),
    (feedgenerator.RssUserland091Feed, AWARE_DATE, "Thu, 11 Aug 2016 00:00:00 -0400"),
    (feedgenerator.RssUserland091Feed, AWARE_DATE_UTC, "Thu, 11 Aug 2016 00:00:00 +0000"),
    (feedgenerator.RssUserland091Feed, NAIVE_DATE, "Thu, 11 Aug 2016 00:00:00 -0000"),
    ])
def test_timezone_handling(generator, date, expected_date_string):
    """
    Test that dates are handled correctly in all Feed generators.
    Also test special cases of no timezone given, vs timezone without offset
    """

    feed = generator(**FIXT_FEED)
    feed.add_item(**(FIXT_ITEM | {'pubdate': date}))
    result = feed.writeString(ENCODING)

    assert expected_date_string in result
