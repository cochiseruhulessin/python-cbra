# Copyright (C) 2021-2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Any

import fastapi


class IRoutable:
    __module__: str = 'cbra.types'
    response_model_by_alias: bool = False

    @classmethod
    def add_to_router(cls, endpoint: Any, router: fastapi.FastAPI | fastapi.APIRouter, **kwargs: Any) -> None:
        raise NotImplementedError