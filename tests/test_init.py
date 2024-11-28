import jazzmin


def test_version():
    """
    Tests getting the version of the installed package in all versions of Python we support.
    """
    assert jazzmin.version >= "0.0.0"
