from rsrc.models import URL
from tests.strategies import strings

urls = strings.map(URL.from_string)
