# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import collections

from .models import Subject
from .types import ISubjectRepository


class MemorySubjectRepository(ISubjectRepository):
    __module__: str = 'cbra.core.iam'
    objects: dict[str, dict[str, Subject]] = collections.defaultdict(dict)

    @classmethod
    def clear(cls) -> None:
        cls.objects = collections.defaultdict(dict)

    def __init__(self):
        self.objects = MemorySubjectRepository.objects