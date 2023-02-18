# Copyright (C) 2021-2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Any

from .endpointtype import EndpointType
from .types import IEndpoint


class Endpoint(IEndpoint, metaclass=EndpointType):
    __abstract__: bool = True
    __module__: str = 'cbra'
    allowed_http_methods: list[str]
    include_in_schema: bool = True

    def __init__(self, **kwargs: Any):
        """Constructor. Called in the router; can contain helpful extra
        keyword arguments, and other things.
        """
        # Go through keyword arguments, and either save their values to our
        # instance, or raise an error.
        for key, value in kwargs.items():
            setattr(self, key, value)