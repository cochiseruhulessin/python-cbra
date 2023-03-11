# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import fastapi

from cbra.core.conf import settings
from cbra.types import Request


__all__: list[str] = [
    'CurrentIssuer'
]


def get_issuer(request: Request) -> str:
    return settings.OAUTH2_ISSUER or\
        f'{request.url.scheme}://{request.url.netloc}'


CurrentIssuer: str = fastapi.Depends(get_issuer)