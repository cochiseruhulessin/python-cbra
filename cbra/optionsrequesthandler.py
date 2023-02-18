# Copyright (C) 2021-2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from .requesthandler import RequestHandler


class OptionsRequestHandler(RequestHandler):
    include_in_schema: bool = False

    def __init__(
        self,
        include_in_schema: bool | None = None
    ):
        super().__init__(
            method='OPTIONS',
            func=self.handle
        )

    async def handle(self):
        pass