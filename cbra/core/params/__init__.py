# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from ..ioc import setting
from ..secretkey import SecretKey


__all__: list[str] = [
    'ApplicationSecretKey'
]

ApplicationSecretKey: SecretKey = SecretKey.depends()

SESSION_COOKIE_AGE: int = setting(
    name='SESSION_COOKIE_AGE',
    default=1209600
)

SESSION_COOKIE_DOMAIN: str | None = setting(
    name='SESSION_COOKIE_DOMAIN',
    default=None
)

SESSION_COOKIE_NAME: str = setting(
    name='SESSION_COOKIE_NAME',
    default='sessionid'
)

SESSION_COOKIE_HTTPONLY: bool = setting(
    name='SESSION_COOKIE_HTTPONLY',
    default=True
)

SESSION_COOKIE_PATH: str = setting(
    name='SESSION_COOKIE_PATH',
    default='/'
)

SESSION_COOKIE_SAMESITE: bool | str | None = setting(
    name='SESSION_COOKIE_SAMESITE',
    default=True
)

SESSION_COOKIE_SECURE: bool = setting(
    name='SESSION_COOKIE_SECURE',
    default=True
)