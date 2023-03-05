# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from types import NotImplementedType

import pydantic

from .basemodel import BaseModel
from .modelidentity import ModelIdentity
from .modelautoassignedidentity import ModelAutoAssignedIdentity
from .modelmetadata import ModelMetadata


class PersistedModel(BaseModel):
    __abstract__: bool = True
    __surrogate__: ModelAutoAssignedIdentity | NotImplementedType | None | int
    __key__: ModelIdentity | NotImplementedType
    __metadata__: ModelMetadata = pydantic.PrivateAttr(
        default_factory=ModelMetadata.initialize
    )

    def natural_key(self) -> tuple[str, ...]:
        raise NotImplementedError