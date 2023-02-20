# Copyright (C) 2021-2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import os
from typing import Any

import uvicorn

os.environ['PYTHON_SETTINGS_MODULE'] = __name__
import cbra.core as cbra


DEPENDENCIES: list[dict[str, Any]] = [
    {
        'name': 'RandomGenerator',
        'qualname': 'os.urandom'
    },
    {
        'name': 'SymbolRequirement',
        'qualname': 'cbra.core.ioc.test.SymbolRequirement'
    },
    {
        'name': 'InstanceRequirement',
        'qualname': 'cbra.core.ioc.test.InstanceRequirement'
    },
    {
        'name': 'NestedRequirement',
        'qualname': 'cbra.core.ioc.test.NestedRequirement'
    },
    {
        'name': 'SingletonRequirement',
        'qualname': 'cbra.core.ioc.test.SingletonRequirement',
        'singleton': True
    },
]

app = cbra.Application(docs_url='/ui')


@app.get('/')
def f(
    injected: Any = cbra.inject('RandomGenerator'),
    symbol: Any = cbra.inject('SymbolRequirement'),
    instance: Any = cbra.instance('InstanceRequirement'),
    nested: Any = cbra.instance('NestedRequirement'),
    singleton: Any = cbra.instance('SingletonRequirement')
):
    print(symbol, instance, nested, singleton)
    return bytes.hex(injected(16))

if __name__ == '__main__':
    uvicorn.run('__main__:app', reload=True) # type: ignore
