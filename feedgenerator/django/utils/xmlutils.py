"""
Utilities for XML generation/parsing.
"""

from xml.sax.saxutils import XMLGenerator, quoteattr

class SimplerXMLGenerator(XMLGenerator):
    def addQuickElement(self, name, contents=None, attrs=None):
        "Convenience method for adding an element with no children"
        if attrs is None: attrs = {}
        self.startElement(name, attrs)
        if contents is not None:
            self.characters(contents)
        self.endElement(name)

    def startElement(self, name, attrs):
        self._write('<' + name)
        # sort attributes for consistent output
        for (name, value) in sorted(attrs.items()):
            self._write(f' {name}={quoteattr(value)}')
        self._write('>')
