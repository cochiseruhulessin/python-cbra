# Copyright (C) 2021-2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import fastapi
import logging

from cbra.core.conf import settings
from cbra.types import IDeferred
from cbra.types import IDependant
from cbra.types import ISessionFactory
from cbra.types import ISessionManager
from cbra.types import Session
from ..params import ApplicationSecretKey
from ..secretkey import SecretKey


class RequestSession(IDeferred, IDependant, ISessionFactory[Session], ISessionManager[Session]):
    __module__: str = 'cbra.core.session'
    cookie_name: str
    data: Session
    key: SecretKey
    logger: logging.Logger = logging.getLogger('uvicorn')
    request: fastapi.Request

    def __init__(
        self,
        request: fastapi.Request,
        key: SecretKey = ApplicationSecretKey
    ) -> None:
        self.cookie_name = settings.SESSION_COOKIE_NAME
        self.key = key
        self.request = request
        self.data = IDeferred.defer(self, 'data')

    async def add_to_response(self, response: fastapi.Response) -> None:
        await self.data.sign(self.key.sign)
        if settings.SESSION_COOKIE_SAMESITE is False:
            samesite = None
        else:
            samesite = settings.SESSION_COOKIE_SAMESITE
        assert samesite is None or isinstance(samesite, str) # nosec
        response.set_cookie(
            key=settings.SESSION_COOKIE_NAME,
            value=self.data.as_cookie(),
            domain=settings.SESSION_COOKIE_DOMAIN,
            max_age=settings.SESSION_COOKIE_AGE,
            httponly=settings.SESSION_COOKIE_HTTPONLY,
            secure=settings.SESSION_COOKIE_SECURE,
            path=settings.SESSION_COOKIE_PATH,
            samesite=samesite # type: ignore
        )

    async def clear(self) -> None:
        self.data = await self.create()

    async def create(self) -> Session:
        self.dirty = True
        return Session.new()

    async def initialize(self) -> None:
        if settings.SESSION_COOKIE_NAME not in self.request.cookies:
            self.data = await self.create()
        else:
            data = Session.parse_cookie(
                self.request.cookies[settings.SESSION_COOKIE_NAME]
            )
            if data is None:
                self.logger.critical(
                    'Session cookie was present but could not be deserialized.'
                )
                self.data = await self.create()
                await self.data.sign(self.key.sign)
            else:
                self.data = data
                self.logger.debug(
                    'Request included a session (id: %s, hmac: %s)',
                    self.data.id, self.data.hmac
                )
            if not await self.data.verify(self.key.verify):
                self.logger.critical(
                    'Session cookie was present but the signature did not '
                    'validate.'
                )
                self.data = await self.create()