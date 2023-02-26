# Copyright (C) 2021-2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import pydantic


class ResourceListMetadata(pydantic.BaseModel):
    #pagination_token: str = pydantic.Field(
    #    default="",
    #    alias='paginationToken',
    #    title='Pagination token',
    #    description=(
    #        'This field represents the pagination token to '
    #        'retrieve the next page of results. If the value '
    #        'is "", it means no further results for the request.'
    #    )
    #)

    next_url: str | None = pydantic.Field(
        default=None,
        alias='nextUrl',
        title="Next URL",
        description=(
            "If the server returned a partial set of the resources "
            "matching the search predicate, the URL at which the next "
            "part of the set can be retrieved. If `nextUrl` is `null`, "
            "them there are no remaining items."
        )
    )