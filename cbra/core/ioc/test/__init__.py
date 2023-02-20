# Copyright (C) 2021-2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import cbra.core as cbra


class SymbolRequirement:
    __module__: str = 'cbra.core.ioc.test'


class InstanceRequirement:
    __module__: str = 'cbra.core.ioc.test'


class SingletonRequirement:
    __module__: str = 'cbra.core.ioc.test'


class NestedRequirement:
    __module__: str = 'cbra.core.ioc.test'

    def __init__(
        self,
        instance: InstanceRequirement = cbra.instance('InstanceRequirement'),
        singleton: SingletonRequirement = cbra.instance('SingletonRequirement')
    ) -> None:
        self.instance = instance
        self.singleton = singleton

    def __repr__(self) -> str:
        return f'NestedRequirement(instance={self.instance}, singleton={self.singleton})'