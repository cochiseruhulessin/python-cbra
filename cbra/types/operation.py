# Copyright (C) 2021-2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import pydantic


class Operation(pydantic.BaseModel):
    """This resource represents a long-running operation
    that is the result of a network API call.
    """
    name: str = pydantic.Field(
        default=...,
        title='Name',
        description=(
            'The server-assigned name, which is only unique within '
            'the same service that originally returns it.'
        )
    )

    done: bool = pydantic.Field(
        default=...,
        title='Done',
        description=(
            'If the value is `false`, it means the operation is still '
            'in progress. If `true`, the operation is completed, and '
            'either `error` or `response` is available.\n\n'
            'The value of this field is always `false` if the **Operation** '
            'object was included in a HTTP response with a 200 status code.'
        )
    )