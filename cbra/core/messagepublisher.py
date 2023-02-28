# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import aorta

from .ioc import inject


class MessagePublisher(aorta.MessagePublisher):
    __module__: str = 'cbra.core'

    def __init__(
        self,
        transport: aorta.types.ITransport = inject('MessageTransport')
    ):
        super().__init__(transport=transport)