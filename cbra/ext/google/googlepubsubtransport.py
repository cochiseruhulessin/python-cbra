# Copyright (C) 2020-2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
"""Declares :class:`GoogleTransport`."""
from typing import Any

from aorta.types import Envelope
from aorta.ext.google import PubsubTransport


class GooglePubsubTransport(PubsubTransport):
    prefix: str
    service_name: str

    def __init__(
        self,
        project: str,
        prefix: str,
        service_name: str
    ):
        self.prefix = prefix
        self.service_name = service_name
        super().__init__(
            project=project,
            topic=self.topic_factory,
            retry_topic=f'{self.prefix}.retry.{service_name}'
        )

    def topic_factory(self, envelope: Envelope[Any]) -> list[str]:
        if envelope.is_event():
            topics: list[str] = [
                f'{self.prefix}.events',
                f'{self.prefix}.events.{envelope.kind}'
            ]
        elif envelope.is_command():
            topics = [f'{self.prefix}.commands.{self.service_name}']
            if envelope.metadata.audience:
                topics = [
                    f'{self.prefix}.commands.{x}'
                    for x in envelope.metadata.audience
                ]
        else:
            raise NotImplementedError
        return topics