# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from .authorizationexception import AuthorizationException


class InvalidResponseTypeRequested(AuthorizationException):
    __module__: str = 'cbra.ext.oauth2.types'
    error: str = 'invalid_request'
    message: str = (
        "The requested 'response_type` is invalid, not allowed by the "
        "server, or not allowed by the client."
    )