# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from datetime import datetime
from datetime import timezone
import functools
from typing import Any

from canonical import EmailAddress
from headless.ext.oauth2.models import OIDCToken
from headless.ext.oauth2.models import SubjectIdentifier

from cbra.core.ioc import instance
from cbra.core.params import CurrentIssuer
from ..memorysubjectrepository import MemorySubjectRepository
from ..models import Subject
from .. import types


class UserOnboardingService:
    """Provides an interface to onboard new and existing subjects."""
    __module__: str = 'cbra.core.iam.services'
    issuer: str
    subjects: types.ISubjectRepository

    def __init__(
        self,
        issuer: str = CurrentIssuer,
        subjects: types.ISubjectRepository = instance(
            name='SubjectRepository',
            missing=MemorySubjectRepository
        )
    ):
        self.issuer = issuer
        self.subjects = subjects
        self.timestamp = datetime.now(timezone.utc)

    def initialize(self, claims: OIDCToken | None = None) -> Subject:
        return Subject(
            kind='User',
            created=self.timestamp,
            seen=self.timestamp,
            claims=claims.dict() if claims else {}
        )
    
    async def sync(
        self,
        issuer: str,
        principal: types.PrincipalType
    ) -> tuple[types.Subject, bool]:
        """Add or create a user with the given *immutable* principal."""
        onboarded = False
        subject = await self.subjects.get(principal)
        if not subject:
            onboarded = True
            subject = self.initialize()
            await self.subjects.persist(subject)
            assert subject.uid is not None
            await self.update(subject, issuer, [principal])
        else:
            onboarded = False
        return subject, onboarded

    async def email(
        self,
        issuer: str,
        email: EmailAddress
    ) -> tuple[types.Subject, bool]:
        """Onboard or update a subject using an validated and trusted
        email address.
        """
        raise NotImplementedError

    async def oidc(self, token: OIDCToken) -> tuple[types.Subject, bool]:
        """Onboard or update a subject using an validated and trusted
        OpenID Connect ID Token.
        """
        subject = None
        found = await self.subjects.find_by_principals(token.principals)
        onboarded = False
        if len(found) > 1:
            # The ID token identified multiple subjects and is thus unusable
            # to establish the identity
            raise NotImplementedError(found)
        if not found:
            onboarded = True
            subject = self.initialize(token)
            await self.subjects.persist(subject)
            assert subject.uid is not None
        else:
            assert len(found) == 1
            subject = await self.subjects.get(found.pop())

        # If the subject is None here, then the subject
        # was deleted, but not its principals. This is
        # for now an unrecoverable error.
        if not subject:
            raise NotImplementedError("Missing Subject for Principal(s)")
        assert subject is not None
        principals = token.principals
        if token.email_verified and token.email:
            # Arbitrarily overwrite the email address here if it is trusted,
            # since we might have received it from other sources.
            subject.add_principal(token.iss, token.email, self.timestamp, trust=True)
            subject.seen = self.timestamp
            principals.remove(token.email)
        await self.update_oidc(subject, token)
        return subject, onboarded

    @functools.singledispatchmethod
    async def can_use(
        self,
        obj: OIDCToken | Subject,
        *args: Any,
        **kwargs: Any
    ) -> bool:
        raise NotImplementedError(type(obj).__name__)

    @can_use.register
    async def can_use_oidc_token(
        self,
        token: OIDCToken
    ) -> bool:
        return len(await self.subjects.find_by_principals(token.principals)) <= 1

    @can_use.register
    async def can_use_for_subject(
        self,
        subject: Subject,
        principals: list[types.PrincipalType]
    ) -> bool:
        """Return a boolean indicating if the principals can be used
        by the subject.
        """
        found = await self.subjects.find_by_principals(principals)
        can_use = not found
        if found:
            can_use = (len(found) == 1) and (found.pop() == subject.uid)
        return can_use

    async def get(self, oidc: OIDCToken) -> Subject | None:
        found = await self.subjects.find_by_principals(oidc.principals)
        if len(found) > 1:
            raise RuntimeError("Principals resolve to multiple Subjects.")
        if not found:
            return None
        return await self.subjects.get(found.pop()) # type: ignore

    async def update_oidc(
        self,
        subject: types.Subject,
        oidc: OIDCToken
    ) -> None:
        assert subject.uid is not None
        subject.seen = self.timestamp
        if oidc.email and not subject.has_principal(oidc.email):
            subject.add_principal(oidc.iss, oidc.email, self.timestamp, oidc.email_verified)
        identifier = SubjectIdentifier(iss=oidc.iss, sub=oidc.sub)
        if not subject.has_principal(identifier):
            subject.add_principal(oidc.iss, identifier, self.timestamp, True)
        await self.subjects.persist(subject)

    async def update(
        self,
        subject: types.Subject,
        iss: str,
        principals: Any,
        trust: bool = False
    ) -> None:
        assert subject.uid is not None
        subject.seen = self.timestamp
        for principal in principals:
            if subject.has_principal(principal):
                continue
            subject.add_principal(iss, principal, self.timestamp, trust=trust)
        await self.subjects.persist(subject)

    async def persist(self, subject: Subject) -> None:
        await self.subjects.persist(subject)