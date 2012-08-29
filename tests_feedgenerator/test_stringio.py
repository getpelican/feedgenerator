# -*- encoding: utf-8 -*-

from __future__ import unicode_literals, print_function

try:
    import unittest2 as unittest
except ImportError:
    import unittest

import six
from six import StringIO

ENCODING = 'utf-8'

S0 = 'hello world, Umlauts: äöüßÄÖÜ, Chinese: 四是四，十是十，十四是十四，四十是四十，四十四隻不識字之石獅子是死的'
S0_BYTES = 'fe fi foe fam'.encode(ENCODING)

print("###", StringIO, "###")

class TestStringIO(unittest.TestCase):

    def test_001_text(self):
        # If we throw unicode into the StringIO buffer, we'll
        # get unicode out of it.
        # Thank god this is the same in Python 2 and 3.
        if six.PY3:
            self.assertEqual(type(S0), str)
        else:
            self.assertEqual(type(S0), unicode)
        buf = StringIO()
        print(S0, file=buf, end="")
        s1 = buf.getvalue()
        self.assertEqual(type(S0), type(s1))
        self.assertEqual(S0, s1)
        if six.PY3:
            self.assertEqual(type(s1), str)
        else:
            self.assertEqual(type(s1), unicode)

    def test_002_bytes(self):
        buf = StringIO()
        print(S0_BYTES, file=buf, end="")
        s1 = buf.getvalue()
        
        if six.PY3:
            # In Python 3 StringIO *ALWAYS* returns str (=text=unicode) !
            # Even if we originally write bytes into the buffer, the value
            # we get out of it has type str!

            # Input is bytes
            self.assertEqual(type(S0_BYTES), bytes)
            # Output is NOT bytes...
            self.assertNotEqual(type(S0_BYTES), type(s1))
            self.assertNotEqual(type(s1), bytes)
            # ...but str!
            self.assertEqual(type(s1), str)
            # So the contents are not equal!
            self.assertNotEqual(S0_BYTES, s1)
            # StringIO coerced bytes into str:
            # b'xyz' ---> "b'xyz'"
            self.assertEqual(str(S0_BYTES), s1)
            # See, the type info is literally present in the output str!
            self.assertEqual("b'" + str(S0_BYTES, encoding=ENCODING) + "'", s1)
            # Coercion is NOT decoding!
            self.assertNotEqual(S0_BYTES.decode(ENCODING), s1)
            self.assertNotEqual(str(S0_BYTES, encoding=ENCODING), s1)
            # These are the same
            self.assertEqual(S0_BYTES.decode(ENCODING), 
                str(S0_BYTES, encoding=ENCODING))
            # Additional note:
            # If we do not specify an encoding when we create a StringIO
            # buffer, Python 3 automatically uses the locale's preferred
            # encoding: locale.getpreferredencoding()
            # Cf. http://docs.python.org/release/3.0.1/library/io.html#io.TextIOWrapper
            # In my case this is the same encoding as the encoding of this source file,
            # namely UTF-8. If on your system both encodings are different, you may 
            # encounter other results than the above.
            #
            # In Python 3.2 the signature of StringIO() has changed. It is no more
            # possible to specify an encoding here.
        else:
            # In Python 2 StringIO returns the type that we originally
            # wrote into the buffer.
            # Here we see that if we write bytes into the buffer, we'll get
            # bytes out of it.
            self.assertEqual(type(S0_BYTES), str)
            self.assertEqual(type(S0_BYTES), type(s1))
            self.assertEqual(type(s1), str)
            self.assertEqual(S0_BYTES, s1)
