# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import ipaddress

from cbra.types import IAuthorizationContext
from cbra.types import ISubject


class AuthenticatedContext(IAuthorizationContext):
    __module__: str = 'cbra.core.iam'

    def __init__(
        self,
        *,
        remote_host: ipaddress.IPv4Address | str | None,
        subject: ISubject
    ):
        if isinstance(remote_host, str):
            remote_host = ipaddress.IPv4Address(remote_host)
        self._host = remote_host
        self._subject = subject

    def get_remote_host(self) -> ipaddress.IPv4Address | None:
        return self._host

    def get_subject(self) -> ISubject:
        return self._subject