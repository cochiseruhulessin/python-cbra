# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from .fatalclientexception import FatalClientException


class InvalidRequest(FatalClientException):
    __module__: str = 'cbra.ext.oauth2.types'

    def __init__(self):
        super().__init__(
            code='invalid_request',
            message=(
                'The request is missing a required parameter '
                'includes an invalid parameter value, includes a parameter more '
                'than once, or is otherwise malformed.'
            )
        )
