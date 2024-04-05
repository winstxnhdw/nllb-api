# pylint: disable=missing-function-docstring

from server.helpers.has_internet_access import has_internet_access


def test_has_internet_access():

    assert all([
        has_internet_access('winstxnhdw/nllb-200-distilled-1.3B-ct2-int8'),
    ]) is True
