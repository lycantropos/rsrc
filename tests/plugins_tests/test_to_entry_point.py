from hypothesis import given
from pkg_resources import EntryPoint

from rsrc.plugins import (Id,
                          serialize_id,
                          to_entry_point)
from . import strategies


@given(strategies.ids, strategies.identifiers, strategies.identifiers)
def test_structure(id_: Id, module_name: str, function_name: str) -> None:
    result = to_entry_point(id_=id_,
                            module_name=module_name,
                            function_name=function_name)

    assert serialize_id(id_) in result
    assert module_name in result
    assert function_name in result
    assert EntryPoint.pattern.fullmatch(result) is not None
