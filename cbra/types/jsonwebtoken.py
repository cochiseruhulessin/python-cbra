# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from .icredential import ICredential


class JSONWebToken(ICredential):
    """An unparsed JSON Web Token."""
    __module__: str = 'cbra.types'
    token: str

    def __init__(self, token: str):
        self.token = token

    def __str__(self) -> str:
        return self.token