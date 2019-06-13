from hypothesis import given

from rsrc.models import URL
from tests.utils import equivalence
from . import strategies


@given(strategies.urls)
def test_basic(url: URL) -> None:
    result = hash(url)

    assert isinstance(result, int)


@given(strategies.urls)
def test_determinism(url: URL) -> None:
    result = hash(url)

    assert result == hash(url)


@given(strategies.urls, strategies.urls)
def test_connection_with_equality(left_url: URL, right_url: URL) -> None:
    assert equivalence(left_url == right_url,
                       hash(left_url) == hash(right_url))
