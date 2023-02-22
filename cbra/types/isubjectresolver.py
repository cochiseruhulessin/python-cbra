# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from .idependant import IDependant
from .irequestprincipal import IRequestPrincipal
from .isubject import ISubject


class ISubjectResolver(IDependant):
    """Resolves an :class:`IRequestPrincipal` to a :class:`ISubject`
    implementation.
    """
    __module__: str = 'cbra.types'

    async def resolve(self, principal: IRequestPrincipal) -> ISubject:
        raise NotImplementedError