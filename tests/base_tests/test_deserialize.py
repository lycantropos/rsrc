import pytest
from hypothesis import given

from rsrc.base import deserialize
from tests import strategies


@given(strategies.strings)
def test_no_support_yet(string: str) -> None:
    with pytest.raises(ValueError):
        deserialize(string)
