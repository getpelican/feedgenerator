from io import StringIO

import pytest

from feedgenerator.django.utils.xmlutils import (
    SimplerXMLGenerator,
    UnserializableContentError,
)


@pytest.mark.parametrize(
    "codepoint",
    [
        0x0000,
        0x0008,
        0x000B,
        0x000C,
        0x000E,
        0x001F,
        0xD800,
        0xDFFF,
        0xFFFE,
        0xFFFF,
    ],
    ids=lambda cp: f"U+{cp:04X}",
)
def test_characters_rejects_invalid_xml_10_characters(codepoint):
    """Characters forbidden by XML 1.0 must raise an exception"""
    output = StringIO()
    generator = SimplerXMLGenerator(output, encoding="utf-8")

    content = f"before{chr(codepoint)}after"

    with pytest.raises(UnserializableContentError) as exc_info:
        generator.characters(content)

    message = str(exc_info.value)

    # The error must identify the offending character.
    assert f"U+{codepoint:04X}" in message

    # The error must report its position in the input string.
    assert "position 6" in message

    # The error must provide the surrounding context.
    assert repr(content) in message


@pytest.mark.parametrize(
    "codepoint",
    [
        0x0009,  # Horizontal tab
        0x000A,  # Line feed
        0x000D,  # Carriage return
        0x0020,  # First printable character
        0xD7FF,  # Last character before surrogate range
        0xE000,  # First character after surrogate range
        0xFFFD,  # Last character in the BMP allowed range
        0x10000,  # First supplementary character
        0x10FFFF,  # Last Unicode code point
    ],
    ids=lambda cp: f"U+{cp:04X}",
)
def test_characters_accepts_valid_xml_10_characters(codepoint):
    """Characters allowed by XML 1.0 must be serialized normally."""
    output = StringIO()
    generator = SimplerXMLGenerator(output, encoding="utf-8")

    content = chr(codepoint)

    generator.characters(content)

    assert output.getvalue() == content
