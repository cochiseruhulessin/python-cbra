# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Any

from headless.ext.oauth2 import Client

import cbra.core as cbra
from .params import ApplicationClient


class TokenHandlerEndpoint(cbra.Endpoint):
    __module__: str = 'cbra.ext.oauth2'
    client: Client = ApplicationClient
    cookie_prefix: str = 'bff'
    path: str
    tags: list[str] = ['OAuth 2.x/OpenID Connect']
    with_options: bool = False

    def set_cookie(self, key: str, *args: Any, **kwargs: Any) -> None:
        return super().set_cookie(f'{self.cookie_prefix}.{key}', *args, **kwargs)

    def delete_cookies(self):
        """Deletes all cookies set by the authorization server."""
        for k in self.request.cookies:
            if not str.startswith(k, self.cookie_prefix):
                continue
            self.delete_cookie(k)