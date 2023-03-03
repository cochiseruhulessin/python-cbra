# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import fastapi

from cbra.types import ETagSet
from cbra.core.conf import settings
from ..secretkey import SecretKey


__all__: list[str] = [
    'ApplicationSecretKey',
    'IfMatchRequestHeader',
    'IfMatchDestructive',
]

ApplicationSecretKey: SecretKey = SecretKey.depends()


def current_issuer(request: fastapi.Request) -> str:
    return settings.OAUTH2_ISSUER\
        or f'{request.url.scheme}://{request.url.netloc}'
CurrentIssuer: str = fastapi.Depends(current_issuer)


IfMatchDestructive: ETagSet = fastapi.Header(
    default=None,
    alias='If-Match',
    description=(
        'With the help of the `ETag` and the `If-Match` headers, '
        'you can detect mid-air edit collisions.\n\n'
        'For example, when editing a resource, the current resource content '
        'may be hashed and put into an `Etag` header in the response:\n\n'
        '```\n'
        'ETag: "33a64df551425fcc55e4d42a148795d9f25f89d4"\n'
        '```\n'
        'When saving changes to the resource the POST, PUT, PATCH or '
        'DELETE request will contain the `If-Match` header containing the '
        '`ETag` values to check freshness against:\n\n'
        '```\n'
        'If-Match: "33a64df551425fcc55e4d42a148795d9f25f89d4"\n'
        '```\n'
        'If the hashes don\'t match, it means that the resource '
        'has been modified in-between and a `412 Precondition Failed` '
        'error response is returned.'
    )
)


IfMatchRequestHeader: ETagSet = fastapi.Header(
    default=None,
    alias='If-Match',
    description=(
        'The server will only return requested resources for `GET` '
        'and `HEAD` methods, if the resource matches one of '
        'the listed `ETag` values. If the conditional does not '
        'match then the `412 (Precondition Failed)` response '
        'is returned.'
    )
)