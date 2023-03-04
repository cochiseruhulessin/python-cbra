# Copyright (C) 2021-2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Any
from typing import TypeVar

from .detailaction import DetailAction
from .iresource import IResource


T = TypeVar('T', bound='CustomAction')


class CustomAction(DetailAction):
    action: str
    status_code: int
    path: str
    use_resource_model: bool = False
    _summary: str

    @property
    def summary(self) -> str:
        return self._summary

    @classmethod
    def fromfunc(
        cls: type[T],
        name: str,
        func: Any
    ) -> T:
        if not hasattr(func, 'action'):
            raise TypeError(f"{name}.{func.__name__} is not an action.")
        return cls(name=name, func=func, **func.action)
    
    def __init__(
        self,
        action: str,
        status_code: int,
        summary: str,
        *args: Any,
        **kwargs: Any
    ):
        self.action = action
        self.path = action
        self.status_code = status_code
        self._summary = summary
        super().__init__(*args, **kwargs)

    def can_mutate(self) -> bool:
        # Custom actions are always detail actions, so POST
        # requests are considered mutations.
        return super().can_mutate() or self.method == "POST"

    def get_url_pattern(
        self,
        prefix: str | None,
        endpoint: type[IResource] | None = None
    ) -> str:
        return f'{super().get_url_pattern(prefix, endpoint)}/{self.path}'

    def is_detail(self) -> bool:
        return True

    def needs_resource(self) -> bool:
        return False