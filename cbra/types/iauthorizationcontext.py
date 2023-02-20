# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from .isubject import ISubject


class IAuthorizationContext:
    __module__: str = 'cbra.types'

    @property
    def subject(self) -> ISubject:
        return self.get_subject()

    def is_authenticated(self) -> bool:
        return self.subject.is_authenticated()

    def get_subject(self) -> ISubject:
        raise NotImplementedError