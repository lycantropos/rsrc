from hypothesis import given

from rsrc.models import URL
from . import strategies


@given(strategies.urls)
def test_round_trip(url: URL) -> None:
    assert url.path_string.startswith('//') or URL.from_string(str(url)) == url
