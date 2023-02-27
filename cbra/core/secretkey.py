# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import re
from typing import Awaitable
from typing import Callable
from typing import TypeVar

from ckms.core import parse_spec
from ckms.core import Keychain
from ckms.utils import b64encode_str
from ckms.utils import b64decode

from cbra.core.conf import settings
from cbra.types import IDependant

T = TypeVar('T', bound='SecretKey')
SIGNING_KEY_NAME: str = 'sig'


class SecretKey(IDependant):
    """The key used by the application to perform various signing operations,
    such as signing a session cookie. Only one instance per application should
    be created, since it used a single instance of its key.
    """
    __module__: str = 'cbra.core.params'
    signing_key_name: str = SIGNING_KEY_NAME
    keychain: Keychain = Keychain()

    @property
    def signing_key(self):
        assert self.keychain.has(self.signing_key_name) # nosec
        return self.keychain.get(self.signing_key_name)

    @classmethod
    async def setup(cls: type[T]) -> T:
        secret_key = settings.SECRET_KEY
        if secret_key and re.match(r'^(local|azure|google)\:', secret_key):
            raise NotImplementedError
        self = cls()
        if secret_key and not cls.keychain.has(cls.signing_key_name):
            spec = parse_spec({
                'provider': 'local',
                'algorithm': 'HS384',
                'kty': 'oct',
                'use': 'sig',

                # TODO: The parameter is incorrectly named but will do for now since
                # there is no public documentation.
                'key': {'cek': secret_key}
            })
            await cls.keychain.add(cls.signing_key_name, spec)
        return self

    def __init__(self):
        self.keychain = SecretKey.keychain

    async def sign(self, value: bytes | str, encoding: str = 'utf-8') -> str:
        """Sign the given value."""
        if isinstance(value, str):
            value = str.encode(value, encoding=encoding)
        return b64encode_str(await self.signing_key.sign(value))

    async def verify(self, signature: bytes | str, message: bytes) -> bool:
        if isinstance(signature, str):
            signature = b64decode(signature)
        return await self.signing_key.verify(signature, message)

    @classmethod
    def __inject__(cls: type[T]) -> Callable[..., Awaitable[T] | T]:
        return cls.setup