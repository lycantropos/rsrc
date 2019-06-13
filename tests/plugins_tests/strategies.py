import keyword
from functools import reduce
from itertools import repeat
from operator import or_
from string import ascii_letters

from hypothesis import strategies

from rsrc.models import URL
from rsrc.plugins import (MAX_ID_PARTS_COUNT,
                          to_id)
from tests.strategies import strings

ids = (reduce(or_, [strategies.tuples(*repeat(strings, times))
                    for times in range(1, len(URL._fields) + 1)])
       .map(lambda parts: to_id(*parts)))
invalid_ids_parts = strategies.lists(strings,
                                     min_size=MAX_ID_PARTS_COUNT + 1)
identifiers_characters = strategies.sampled_from(ascii_letters + '_')
identifiers = (strategies.text(identifiers_characters,
                               min_size=1)
               .filter(str.isidentifier)
               .filter(lambda string: not keyword.iskeyword(string)))
