# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from cbra.core.iam import SubjectResolver
from cbra.core.iam import RequestSubject
from cbra.core.ioc import instance
from cbra.core.ioc import override
from cbra.types import NullSubject
from cbra.types import SessionRequestPrincipal

from .datastoresubjectrepository import DatastoreSubjectRepository


class DatastoreSubjectResolver(SubjectResolver):
    """A :class:`~cbra.core.iam.SubjectResolver` implementation
    that uses Google Datastore as its storage backend.
    """
    __module__: str = 'cbra.ext.google'
    repo: DatastoreSubjectRepository

    @override(SubjectResolver.__init__)
    def __init__(
        self,
        repo: DatastoreSubjectRepository = instance('SubjectRepository')
    ) -> None:
        self.repo = repo

    async def resolve_session(
        self,
        principal: SessionRequestPrincipal
    ) -> RequestSubject | NullSubject:
        if principal.claims.uid is None:
            return NullSubject()
        subject = await self.repo.resolve(principal.claims.uid)
        if subject is None:
            return NullSubject()
        assert subject.uid is not None # nosec
        return RequestSubject(
            id=str(subject.uid),
            email=principal.claims.email,
            principal=principal
        )