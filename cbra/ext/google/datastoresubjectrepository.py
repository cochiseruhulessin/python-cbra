# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import functools
from typing import Any
from typing import AsyncGenerator

from canonical import EmailAddress
from google.cloud.datastore import Query
from headless.ext.oauth2.models import SubjectIdentifier

from cbra.types import IModelRepository
from cbra.core.iam import ISubjectRepository
from cbra.core.iam.models import Principal
from cbra.core.iam.models import Subject
from .datastorerepository import DatastoreRepository


class DatastoreSubjectRepository(
    DatastoreRepository,
    ISubjectRepository,
    IModelRepository[Subject]
):
    __module__: str = 'cbra.ext.google'

    @functools.singledispatchmethod # type: ignore
    async def get(self, principal: Any) -> Subject | None:
        if principal is None: return None
        raise NotImplementedError(f'{principal.__module__}.{type(principal).__name__}')

    @get.register
    async def get_by_email(self, principal: EmailAddress) -> Subject | None:
        query = self.query('Principal')
        query.add_filter('spec.kind', '=', 'EmailAddress') # type: ignore
        query.add_filter('spec.email', '=', str(principal)) # type: ignore
        dao = await self.one(Principal, query)
        if dao is None:
            return None
        return await self.get(dao.subject)

    @get.register
    async def get_by_identifier(self, principal: SubjectIdentifier) -> Subject | None:
        query = self.query('Principal')
        query.add_filter('spec.kind', '=', 'SubjectIdentifier') # type: ignore
        query.add_filter('spec.iss', '=', principal.iss) # type: ignore
        query.add_filter('spec.sub', '=', principal.sub) # type: ignore
        dao = await self.one(Principal, query)
        if dao is None:
            return None
        return await self.get(dao.subject)

    @get.register
    async def get_by_uid(self, uid: int) -> Subject | None:
        assert isinstance(uid, int), repr(uid)
        obj = await self.get_model_by_key(Subject, uid)
        if obj is None:
            return None
        assert obj.uid is not None
        async for principal in self.get_principals(obj.uid):
            obj.principals.add(principal)
        return obj

    async def get_principals(self, subject_id: int) -> AsyncGenerator[Principal, None]:
        query = self.query(Principal)
        query.add_filter('subject', '=', subject_id) # type: ignore
        for entity in await self.run_in_executor(query.fetch): # type: ignore
            yield self.restore(Principal, entity)

    async def resolve(self, identity: int | str) -> Subject | None:
        """Resolve a principal to a global subject identifier."""
        return await self.get(int(identity))

    async def find_by_principals(
        self,
        principals: list[Any]
    ) -> set[int]:
        subjects: set[int] = set()
        for principal in principals:
            query = self.query(Principal)
            self.filter_principal(principal, query)
            subjects.update([
                int(x['subject']) async for x in self.execute(query, dict[str, int])
            ])
        return subjects

    async def persist(self, instance: Subject) -> Subject:
        await self.put(instance, exclude={'principals', 'uid'})
        assert instance.uid is not None
        await self.delete([self.model_key(x) for x in instance._removed_principals]) # type: ignore
        for principal in instance.principals:
            await self.put(principal, exclude={'id'})
        return instance

    @functools.singledispatchmethod
    def filter_principal(
        self,
        principal: EmailAddress | SubjectIdentifier,
        query: Query
    ) -> None:
        raise NotImplementedError(type(principal).__name__)

    @filter_principal.register
    def filter_emailaddress(
        self,
        principal: EmailAddress,
        query: Query
    ) -> None:
        query.add_filter('spec.kind', '=', 'EmailAddress') # type: ignore
        query.add_filter('spec.email', '=', str(principal)) # type: ignore

    @filter_principal.register
    def filter_subjectidentifier(
        self,
        principal: SubjectIdentifier,
        query: Query
    ) -> None:
        query.add_filter('spec.kind', '=', 'SubjectIdentifier') # type: ignore
        query.add_filter('spec.iss', '=', principal.iss) # type: ignore
        query.add_filter('spec.sub', '=', principal.sub) # type: ignore