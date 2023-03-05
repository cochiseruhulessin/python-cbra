# Copyright (C) 2016-2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import aorta
import pytest

from cbra.core import MessageRunner


class UnregisteredEvent(aorta.Event):
    pass


class Sewer(aorta.Sewer):
    pass


aorta.register(Sewer)


@pytest.mark.asyncio
async def test_runner_handles_unregistered_event(
    runner: MessageRunner
):
    envelope = UnregisteredEvent().envelope()
    await runner.run(envelope)