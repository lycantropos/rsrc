from typing import Iterable

import pytest
from hypothesis import given

from rsrc.plugins import to_id
from . import strategies


@given(strategies.invalid_ids_parts)
def test_invalid_arguments_count(parts: Iterable[str]) -> None:
    with pytest.raises(ValueError):
        to_id(*parts)
