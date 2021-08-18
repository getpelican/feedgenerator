import os
import tempfile
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

FN_PREFIX = 'feed_py3-'

# Usage example in feedgenerator docs opens the file in text mode, not binary.
# So we do this here likewise.
fd, filename = tempfile.mkstemp(prefix=FN_PREFIX, suffix='.txt', text=True)
try:
    fh = os.fdopen(fd, 'w')
    feed.write(fh, 'utf-8')
finally:
    fh.close()
