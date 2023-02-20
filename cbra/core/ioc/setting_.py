# Copyright (C) 2021-2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import importlib

from .container import Container
from .dependency import Dependency
from .injected import Injected


class Setting(Injected):
    __module__: str = 'cbra.core.ioc'

    def add_to_container(self, container: Container) -> None:
        if container.has(self.name):
            # TODO: This basically cover the user case where the implementer
            # override the dependency from somewhere in the code. This is
            # currently only used in the examples.
            self.ref = container.require(self.name)
            return
        try:
            config = importlib.import_module('cbra.core.conf')
            self.ref = Dependency(
                name=self.name,
                qualname=f'cbra.core.conf.settings.{self.name}',
                symbol=getattr(config.settings, self.name)
            )
        except (AttributeError, ImportError):
            if self.missing == NotImplemented:
                raise
            self.ref = Dependency(
                name=self.name,
                qualname=f'cbra.core.conf.settings.{self.name}',
                symbol=self.missing
            )