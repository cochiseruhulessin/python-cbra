# Copyright (C) 2020-2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import pytest

import aorta
from cbra.ext.google import GooglePubsubTransport


class GoogleEvent(aorta.Event):
    pass


class GoogleCommand(aorta.Command):
    pass


@pytest.fixture
def transport() -> GooglePubsubTransport:
    return GooglePubsubTransport(
        project='project',
        prefix='prefix',
        service_name='service_name'
    )


def test_topics_event(
    transport: GooglePubsubTransport
):
    envelope = GoogleEvent().envelope()
    topics = set(transport.get_topics(envelope))
    assert topics == {
        "projects/project/topics/prefix.events",
        "projects/project/topics/prefix.events.GoogleEvent"
    }


def test_topics_command(
    transport: GooglePubsubTransport
):
    envelope = GoogleCommand().envelope()
    topics = set(transport.get_topics(envelope))
    assert topics == {
        "projects/project/topics/prefix.commands.service_name",
    }


def test_topics_command_audience(
    transport: GooglePubsubTransport
):
    envelope = GoogleCommand().envelope()
    envelope.metadata.audience = ['foo']
    topics = set(transport.get_topics(envelope))
    assert topics == {
        "projects/project/topics/prefix.commands.foo",
    }


def test_topics_command_audiences(
    transport: GooglePubsubTransport
):
    envelope = GoogleCommand().envelope()
    envelope.metadata.audience = ['foo', 'bar', 'baz']
    topics = set(transport.get_topics(envelope))
    assert topics == {
        "projects/project/topics/prefix.commands.foo",
        "projects/project/topics/prefix.commands.bar",
        "projects/project/topics/prefix.commands.baz",
    }