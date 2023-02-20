# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import datetime
import ipaddress

from .isubject import ISubject


class IAuthorizationContext:
    __module__: str = 'cbra.types'
    timestamp: datetime.datetime

    @property
    def remote_host(self) -> ipaddress.IPv4Address | None:
        """A :class:`~ipaddress.IPv4Address` instance specifying the remote
        host from which a request was made, or ``None`` if there is no
        network request.
        """
        return self.get_remote_host()

    @property
    def subject(self) -> ISubject:
        """The subject that was resolved from the principal and the
        credential.
        """
        return self.get_subject()

    async def authorize(self) -> bool:
        """Fetch the permissions, roles and other authorizations for the current
        subject. When implementing :class:`IAuthorizationContext`, provide an
        awaitable object to the constructor that knows how to retrieve the
        authorizations.
        """
        raise NotImplementedError

    def is_authenticated(self) -> bool:
        """Return a boolean indicating if the request is authenticated."""
        return self.subject.is_authenticated()

    def get_remote_host(self) -> ipaddress.IPv4Address | None:
        raise NotImplementedError

    def get_subject(self) -> ISubject:
        raise NotImplementedError

    def has_permission(self, name: str) -> bool:
        """Return a boolean indicating if the context has the given
        permission. This method should always be invoked after
        :meth:`authorize()`.
        """
        raise NotImplementedError