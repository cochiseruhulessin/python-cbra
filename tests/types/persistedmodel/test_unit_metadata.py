# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import pytest

from cbra.types import ModelInspector
from .conftest import Parent


inspector: ModelInspector = ModelInspector()


@pytest.mark.parametrize("obj", [Parent, Parent()])
def test_get_column_fields(obj: Parent | type[Parent]):
    fields = inspector.get_column_fields(obj)
    assert 'children' not in fields
    assert 'foo' in fields
    assert 'bar' in fields
    assert 'baz' in fields


@pytest.mark.parametrize("obj", [Parent, Parent()])
def test_has_children(obj: Parent | type[Parent]):
    assert inspector.has_children(obj)


def test_must_insert_on_pristine():
    assert inspector.is_insert(Parent())