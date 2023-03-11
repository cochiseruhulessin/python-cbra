# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import cast
from typing import Any
from typing import TypeVar

import cbra.core as cbra
from cbra.core.iam.types import ISubjectRepository
from cbra.core.iam.types import Subject
from .types import IAuthorizationServerStorage


T = TypeVar('T')


class AuthorizationServerStorage:
    __module__: str = 'cbra.ext.oauth2'
    app: IAuthorizationServerStorage
    public: IAuthorizationServerStorage
    subjects: ISubjectRepository

    def __init__(
        self,
        app: IAuthorizationServerStorage = cbra.instance(
            name='_ApplicationStorage'
        ),
        public: IAuthorizationServerStorage = cbra.instance(
            name='AuthorizationServerStorage'
        ),
        subjects: ISubjectRepository = cbra.instance(
            name='SubjectRepository'
        )
    ):
        self.app = app
        self.public = public
        self.subjects = subjects

    async def get_subject(self, *args: Any, **kwargs: Any) -> None | Subject:
        return await self.subjects.get(*args, **kwargs)

    async def get(
        self,
        cls: type[T],
        *args: Any,
        **kwargs: Any
    ) -> T | None:
        if cls == Subject:
            return cast(T, await self.get_subject(*args, **kwargs))
        return await self.app.get(cls, *args, **kwargs)\
            or await self.public.get(cls, *args, **kwargs)

    async def persist(self, obj: Any) -> None:
        return await self.public.persist(obj)