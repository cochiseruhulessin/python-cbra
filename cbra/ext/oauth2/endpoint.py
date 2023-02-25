# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
"""
.. _ref-guides-integrating-an-oauth2-authorization-server

=============================================
Integrating an OAuth 2.x authorization server
=============================================
"""
import cbra.core as cbra
from cbra.core.conf import settings
from cbra.core.iam import ISubjectRepository
from cbra.core.iam.types import IUserOnboardingService
from cbra.core.iam.services import UserOnboardingService
from .memorystorage import MemoryStorage
from .types import IAuthorizationServerStorage


class AuthorizationServerEndpoint(cbra.Endpoint):
    onboard: IUserOnboardingService = cbra.ioc.instance(
        name='SubjectOnboardingService',
        missing=UserOnboardingService
    )
    storage: IAuthorizationServerStorage = cbra.ioc.instance(
        name='AuthorizationServerStorage',
        missing=MemoryStorage
    )
    subjects: ISubjectRepository = cbra.ioc.instance('SubjectRepository')

    def get_issuer(self) -> str:
        return settings.OAUTH2_ISSUER or\
            f'{self.request.url.scheme}://{self.request.url.netloc}'