# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Any

import pydantic
from fastapi.security.utils import get_authorization_scheme_param

from .irequestprincipal import IRequestPrincipal


class HTTPHeaderPrincipal(IRequestPrincipal, pydantic.BaseModel):
    """A :class:`IRequestPrincipal` that is provided through the
    ``Authorization`` HTTP request header.
    """
    @pydantic.root_validator(pre=True)
    def preprocess(
        cls,
        values: dict[str, Any]
    ) -> dict[str, Any]:
        return cls.parse_authorization_header(values)

    @classmethod
    def parse_authorization_header(
        cls,
        values: dict[str, Any]
    ) -> dict[str, Any]:
        headers = values.get('headers') or {}
        if not headers.get('Authorization'):
            raise ValueError('no Authorization header.')
        scheme, param = get_authorization_scheme_param(headers['Authorization'])
        if not scheme or not param:
            raise ValueError('the Authorization header was malformed.')
        values.update(cls.parse_scheme(values, str.lower(scheme), param))
        return values

    @classmethod
    def parse_scheme(
        cls,
        values: dict[str, Any],
        scheme: str,
        value: str
    ) -> dict[str, Any]:
        raise NotImplementedError
        
