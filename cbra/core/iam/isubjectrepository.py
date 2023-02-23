# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Any
from typing import AsyncGenerator

from cbra.types import IModelRepository
from .models import Subject
from .models import Principal


class ISubjectRepository(IModelRepository[Subject]):
    __module__: str = 'cbra.core.iam'
    model: type[Subject] = Subject

    def get_principals(self, subject_id: int) -> AsyncGenerator[Principal, None]:
        """Return the list of principals that are registered for a
        subject.
        """
        raise NotImplementedError

    async def find_by_principals(
        self,
        principals: list[Any]
    ) -> set[int]:
        """Identify subjects by the given principals and return a
        list of integers representing the subject identifiers.
        """
        raise NotImplementedError