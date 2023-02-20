# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import ipaddress

from .iauthorizationcontext import IAuthorizationContext
from .nullsubject import NullSubject


class UnauthenticatedAuthorizationContext(IAuthorizationContext):
    __module__: str = 'cbra.types'

    def __init__(
        self,
        remote_host: ipaddress.IPv4Address | str | None = None
    ):
        if isinstance(remote_host, str):
            remote_host = ipaddress.IPv4Address(remote_host)
        self._remote_host = remote_host

    def get_remote_host(self) -> ipaddress.IPv4Address | None:
        return self._remote_host

    def get_subject(self) -> NullSubject:
        return NullSubject()