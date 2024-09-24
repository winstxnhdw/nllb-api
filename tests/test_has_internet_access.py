# pylint: disable=missing-function-docstring

from pytest import mark

from server.utils.has_internet_access import has_internet_access


@mark.parametrize(
    'model_name',
    ['winstxnhdw/nllb-200-distilled-1.3B-ct2-int8', 'facebook/fasttext-language-identification'],
)
def test_has_internet_access(model_name: str):
    assert has_internet_access(model_name)
