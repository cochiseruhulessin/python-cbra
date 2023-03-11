# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import fastapi

from cbra.types import IDependant


__all__: list[str] = [
    'DownstreamError'
]

class Error(IDependant):
    error: str

    def __init__(self, error: str):
        self.error = error

    @classmethod
    def __inject__(cls): # type: ignore
        return cls.fromrequest
    
    @classmethod
    def fromrequest(
        cls,
        error: str | None = fastapi.Query(
            default=None,
            title="Error code",
            description=(
                "The error code returned by the authorization server if "
                "the user cancelled the request, refused consent, or "
                "failed to authenticate."
            )
        )
    ):
        return cls(error) if error else None


DownstreamError: Error | None = Error.depends()