"""
Utilities for XML generation/parsing.
"""

import re
from xml.sax.saxutils import XMLGenerator

INVALID_XML_CHARS = re.compile(
    r"[^\x09\x0A\x0D\x20-\uD7FF\uE000-\uFFFD\U00010000-\U0010FFFF]"
)


class UnserializableContentError(ValueError):
    pass


class SimplerXMLGenerator(XMLGenerator):
    def addQuickElement(self, name, contents=None, attrs=None):
        """Convenience method for adding an element with no children"""
        if attrs is None:
            attrs = {}
        self.startElement(name, attrs)
        if contents is not None:
            self.characters(contents)
        self.endElement(name)

    def characters(self, content):
        """Generate XML content

        :raises: UnserializableContentErrorand:
            If characters forbidden by XML 1.0 are detected.
        .. seealso:: https://www.w3.org/TR/xml/#charsets
        """
        match = INVALID_XML_CHARS.search(content) if content else None
        if match:
            pos = match.start()
            char = content[pos]
            context = content[max(0, pos - 30) : pos + 30]

            raise UnserializableContentError(
                f"Character U+{ord(char):04X} at position {pos} "
                f"is not supported in XML 1.0. Context: {context!r}"
            )
        XMLGenerator.characters(self, content)

    def startElement(self, name, attrs):
        # Sort attrs for a deterministic output.
        sorted_attrs = dict(sorted(attrs.items())) if attrs else attrs
        super().startElement(name, sorted_attrs)
