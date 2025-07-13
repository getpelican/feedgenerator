from feedgenerator.django.utils.encoding import is_protected_type

def test_none_type():
    assert is_protected_type(None)
