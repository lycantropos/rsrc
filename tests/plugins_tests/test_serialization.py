from hypothesis import given

from rsrc.plugins import (Id,
                          deserialize_id,
                          serialize_id)
from . import strategies


@given(strategies.ids)
def test_round_trip(id_: Id) -> None:
    assert deserialize_id(serialize_id(id_)) == id_
