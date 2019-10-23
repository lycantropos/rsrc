from abc import (ABC,
                 abstractmethod)
from pathlib import PurePosixPath
from typing import (Any,
                    AnyStr,
                    Generic,
                    IO,
                    Iterable,
                    Iterator,
                    Optional,
                    Type,
                    TypeVar,
                    Union)
from urllib.parse import (quote,
                          quote_plus,
                          unquote,
                          unquote_plus,
                          urlparse,
                          urlunparse)

from memoir import cached
from reprit.base import generate_repr

from .hints import Domain


# not using `namedtuple` to be weak referencable
class URL:
    _fields = ('scheme', 'authority', 'path_string',
               'params', 'query', 'fragment')
    __slots__ = ('_tuple', '__weakref__')

    AUTHORITY_SEPARATOR = '@'

    # added for auto-completion support,
    # each of them will be overwritten afterwards in cycle
    # and made a `property`
    scheme = ''
    authority = ''
    path_string = ''
    params = ''
    query = ''
    fragment = ''

    for index, field in enumerate(_fields):
        locals()[field] = property(
                lambda self, index=index: self._tuple[index])
    del index, field

    def __init__(self,
                 scheme: str,
                 authority: str,
                 path_string: str,
                 params: str,
                 query: str,
                 fragment: str) -> None:
        self._tuple = (scheme, authority, path_string, params, query, fragment)

    def __hash__(self) -> int:
        """Returns hash of the URL."""
        return hash(self._tuple)

    def __eq__(self, other: 'URL') -> bool:
        """Checks if the URL is equal to the given one."""
        if not isinstance(other, URL):
            return NotImplemented
        return self._tuple == other._tuple

    def __str__(self) -> str:
        """Returns human-readable string representation of the URL."""
        return urlunparse(self._replace(path_string=quote(self.path_string,
                                                          '/%'),
                                        query=quote_plus(self.query, ':&='))
                          ._tuple)

    __repr__ = generate_repr(__init__)
    __repr__.__doc__ = """Returns string representation of the URL."""

    def _replace(self, **kwargs: str) -> 'URL':
        """Returns URL with fields replaced by given values."""
        return type(self)(*map(kwargs.pop, self._fields, self._tuple))

    def join(self, part: str, *parts: str) -> 'URL':
        """Returns URL with path combined with given parts."""
        return self._replace(path_string=str(self.path.joinpath(part, *parts)),
                             params='',
                             query='',
                             fragment='')

    @cached.property_
    def path(self) -> PurePosixPath:
        """Returns URL path."""
        return PurePosixPath(self.path_string)

    @cached.property_
    def without_credentials(self) -> 'URL':
        """Returns URL without credentials."""
        authority = self.authority.rsplit(self.AUTHORITY_SEPARATOR)[-1]
        return self._replace(authority=authority)

    @classmethod
    def from_string(cls: Type[Domain], string: str) -> Domain:
        """Constructs URL from given string."""
        raw = urlparse(string)
        return cls(scheme=raw.scheme,
                   authority=raw.netloc,
                   path_string=unquote(raw.path),
                   params=raw.params,
                   query=unquote_plus(raw.query),
                   fragment=raw.fragment)


class Base(ABC):
    @property
    @abstractmethod
    def url(self) -> URL:
        """Returns resource's URL."""

    @abstractmethod
    def exists(self) -> bool:
        """Checks if the resource is accessible and exists."""

    @abstractmethod
    def __repr__(self) -> str:
        """Returns string representation of the resource."""

    @abstractmethod
    def __str__(self) -> str:
        """Returns human-readable string representation of the resource."""

    @abstractmethod
    def __hash__(self) -> int:
        """Returns hash of the resource."""

    @abstractmethod
    def __eq__(self, other: 'Base') -> bool:
        """Checks if the resource is equal to the given one."""

    @classmethod
    @abstractmethod
    def from_string(cls: Type[Domain], string: str) -> Domain:
        """Constructs resource from given string."""


class Container(Base):
    @abstractmethod
    def join(self, part: str, *parts: str) -> Base:
        """Returns resource combined with given parts."""

    def __truediv__(self, part: str) -> Base:
        """Returns resource combined with given part."""
        if not isinstance(part, str):
            return NotImplemented
        return self.join(part)

    @abstractmethod
    def __iter__(self) -> Iterator[Base]:
        """Returns contained resources."""


Element = TypeVar('Element')


class Stream(Base, Generic[Element]):
    @abstractmethod
    def open(self, **kwargs) -> Iterable[Element]:
        """Returns contained elements."""

    @abstractmethod
    def send(self, destination: Base, **kwargs: Any) -> None:
        """Sends the stream to the given destination."""

    @abstractmethod
    def receive(self, source: Base, **kwargs: Any) -> None:
        """Receives the stream from the given source."""


class FileLikeStream(Stream[AnyStr]):
    @abstractmethod
    def open(self,
             *,
             binary_mode: bool = False,
             encoding: Optional[str] = None,
             **kwargs: Any) -> IO:
        """Returns file-like object from the stream."""


Resource = Union[Stream, Container]
