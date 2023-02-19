# Copyright (C) 2021-2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Any


class Persister:

    async def persist(
        self,
        resource: Any,
        create: bool = False
    ) -> Any:
        raise NotImplementedError(
            f'Implement {type(self).__name__}.persist() '
            f'to persist {type(resource).__name__} resources.'
        )