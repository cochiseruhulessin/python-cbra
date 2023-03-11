# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import fastapi
from ckms.core import Keychain
from ckms.core import parse_dsn

from cbra.core.conf import settings
from ..const import DEFAULT_SIGNING_KEY


__all__: list[str] = ['ServerKeychain']


keychain: Keychain = Keychain()


async def get():
    if settings.OAUTH2_SIGNING_KEY is None:
        raise TypeError("Declare OAUTH2_SIGNING_KEY in settings or environment.")
    keychain.configure({
        DEFAULT_SIGNING_KEY: parse_dsn(settings.OAUTH2_SIGNING_KEY)
    })
    await keychain
    return keychain


ServerKeychain: Keychain = fastapi.Depends(get)