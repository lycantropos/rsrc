from hypothesis import given

from rsrc.models import URL
from . import strategies


@given(strategies.urls, strategies.strings, strategies.strings)
def test_chaining(url: URL, first_part: str, second_part: str) -> None:
    assert (url.join(first_part, second_part)
            == url.join(first_part).join(second_part))
