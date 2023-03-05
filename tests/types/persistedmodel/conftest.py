# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from cbra.types import PersistedModel



class GreatGrandChild(PersistedModel):
    pass


class GrandChild(PersistedModel):
    children: list[GreatGrandChild]


class Child(PersistedModel):
    children: list[GrandChild] = []


class Parent(PersistedModel):
    foo: int | None = None
    bar: int = 1
    baz: str = 'baz'
    children: list[Child] = []