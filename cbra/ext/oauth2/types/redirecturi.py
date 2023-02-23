# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import ipaddress
import urllib.parse
from typing import Any
from typing import Callable
from typing import Generator
from typing import TypeVar

from pydantic.validators import str_validator

T = TypeVar('T', bound='RedirectURI')


OOB_URLS: set[str] = {
    "urn:ietf:wg:oauth:2.0:oob",
    "urn:ietf:wg:oauth:2.0:oob:auto"
}


class RedirectURI(str):
    __module__: str = 'cbra.ext.oauth2.types'
    value: urllib.parse.ParseResult
    params: dict[str, str]

    @classmethod
    def __modify_schema__(
        cls,
        field_schema: dict[str, Any]
    ) -> None:
        field_schema.update( # pragma: no cover
            title='Email Address',
            type='string',
            format='email'
        )

    @classmethod
    def __get_validators__(cls: type[T]) -> Generator[Callable[..., str | T], None, None]:
        yield str_validator
        yield cls.validate

    @classmethod
    def validate(cls: type[T], v: str) -> T:
        if len(v) > 2048:
            raise ValueError("value is too long to be a valid URL.")
        if v in OOB_URLS:
            raise ValueError('OOB is a security risk.')

        p = urllib.parse.urlparse(v)
        if not p.scheme or not p.netloc:
            raise ValueError('not a valid URL.')
        if p.query:
            raise ValueError('query parameters must not be used.')
        if p.fragment:
            raise ValueError('fragments must not be used.')

        # Check if the value is an IP address.
        if p.hostname:
            try:
                ip = ipaddress.ip_address(p.hostname)
            except ValueError:
                # Not a valid ip address. The hostname points to a domain
                if p.scheme != 'https':
                    raise ValueError('the https scheme must be used.')
            else:
                if not ip.is_loopback and p.scheme != 'https':
                    raise ValueError('the https scheme must be used.')

            if p.hostname == 'localhost':
                # Clients should use loopback IP literals rather than the
                # string localhost as described in Section 8.4.2.
                # (OAuth 2.1 draft).
                raise ValueError('local redirect URIs must use loopback IP literals.')

        return cls(p)

    def redirect(self, **params: str) -> str:
        """Create a redirect URI with the given params."""
        p = list(urllib.parse.urlparse(self))
        p[4] = urllib.parse.urlencode(params, quote_via=urllib.parse.quote)
        return urllib.parse.urlunparse(p)

    def __repr__(self) -> str: # pragma: no cover
        return f'RedirectURI({self})'