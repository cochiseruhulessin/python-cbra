# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from headless.ext import oauth2

from cbra.core.iam.types import Subject
from .authorizationcodecallbackendpoint import AuthorizationCodeCallbackEndpoint


class OIDCRegistrationEndpoint(AuthorizationCodeCallbackEndpoint):
    """Registers a new user or authenticates an existing user with
    a redirect response from an OpenID Connect authorization
    server.
    """
    __module__: str = 'cbra.ext.oauth2'
    summary: str = 'OIDC User Registration Endpoint'

    async def on_success(
        self,
        client: oauth2.Client,
        access_token: oauth2.BearerTokenCredential,
        id_token: oauth2.OIDCToken | None = None
    ) -> None:
        if id_token is None:
            raise NotImplementedError
        subject, onboarded = await self.onboard.oidc(id_token)
        if onboarded:
            await self.on_registered(subject, id_token)
        else:
            await self.on_returning(subject, id_token)

    async def on_registered(
        self,
        subject: Subject,
        token: oauth2.OIDCToken
    ):
        """Invoked when the subject described by the OIDC ID Token
        is a new user.
        """
        await self.session
        self.session.update({
            **token.dict(exclude_none=True),
            'iss': self.get_issuer(),
            'sub': str(subject.uid),
        })

    async def on_returning(
        self,
        subject: Subject,
        token: oauth2.OIDCToken
    ):
        """Invoked when the subject described by the OIDC ID Token
        is a returning user.
        """
        await self.session
        self.session.update({
            **token.dict(include={'email', 'email_verified'}, exclude_none=True),
            'iss': self.get_issuer(),
            'sub': str(subject.uid),
        })