from hypothesis import given

from rsrc.models import URL
from tests.utils import implication
from . import strategies


@given(strategies.urls)
def test_reflexivity(url: URL) -> None:
    assert url == url


@given(strategies.urls, strategies.urls)
def test_symmetry(left_url: URL, right_url: URL) -> None:
    assert implication(left_url == right_url, right_url == left_url)


@given(strategies.urls, strategies.urls, strategies.urls)
def test_transitivity(left_url: URL, mid_url: URL, right_url: URL) -> None:
    assert implication(left_url == mid_url and mid_url == right_url,
                       left_url == right_url)
