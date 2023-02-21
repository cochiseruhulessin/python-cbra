# Copyright (C) 2020-2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
"""Declares :class:`GoogleTransport`."""
from aorta.transport import GoogleTransport
from aorta.models import Message


class GooglePubsubTransport(GoogleTransport):
    command_project: str
    command_topic: str
    events_project: str
    events_topic: str

    def __init__(
        self,
        project: str,
        command_topic: str,
        events_topic: str,
        command_project: str | None = None,
        events_project: str | None = None
    ):
        super().__init__(project=project, topic_path=None)
        self.command_project = command_project or project
        self.command_topic = command_topic
        self.events_project = events_project or project
        self.events_topic = events_topic

    def get_topics(self, message: Message):
        topics = [self.events_topic, f'{self.events_topic}.{message.kind}']
        project = self.events_project
        if message.is_command():
            project = self.command_project
            topics = [self.command_topic]
        return [self.client.topic_path(project, x) for x in topics]
