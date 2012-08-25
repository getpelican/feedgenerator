# -*- encoding: utf-8 -*-
import feedgenerator
feed = feedgenerator.Rss201rev2Feed(
    title="Poynter E-Media Tidbits",
    link="http://www.poynter.org/column.asp?id=31",
    description="""A group Weblog by the sharpest minds in online media/journalism/publishing.
    Umlauts: äöüßÄÖÜ
    Chinese: 老师是四十四，是不是？
    Finnish: Mustan kissan paksut posket. (ah, no special chars) Kärpänen sanoi kärpäselle: tuu kattoon kattoon ku kaveri tapettiin tapettiin.
    """,
    language="en",
)
feed.add_item(
    title="Hello",
    link="http://www.holovaty.com/test/",
    description="Testing."
)
with open('test.rss', 'w') as fp:
    feed.write(fp, 'utf-8')

