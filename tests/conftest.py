# Copyright (C) 2021-2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import asyncio

import aorta
import pytest

import cbra.core as cbra


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def publisher() -> cbra.MessagePublisher:
    return cbra.MessagePublisher(
        transport=aorta.NullTransport(),
        request=None # type: ignore
    )


@pytest.fixture
def runner(
    publisher: cbra.MessagePublisher
) -> aorta.types.IRunner:
    return cbra.MessageRunner(
        publisher=publisher,
        request=None # type: ignore
    )