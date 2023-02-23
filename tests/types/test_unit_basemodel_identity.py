# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import secrets

import pytest
import pydantic

from cbra.types import BaseModel


# Set defaults on the test model so we can always instantiate
# them.
class ModelWithScalarIdentity(BaseModel):
    id: int = pydantic.Field(1, primary_key=True)
    non_key_field: str = pydantic.Field(
        default_factory=lambda: secrets.token_urlsafe(48)
    )


class ModelWithCompositeIdentity(BaseModel):
    id: int = pydantic.Field(1, primary_key=True)
    item_id: int = pydantic.Field(2, primary_key=True)
    non_key_field: str = pydantic.Field(
        default_factory=lambda: secrets.token_urlsafe(48)
    )


class ModelWithNestedIdentity(BaseModel):
    id: int = pydantic.Field(1, primary_key=True)
    child: ModelWithScalarIdentity = pydantic.Field(
        default_factory=ModelWithScalarIdentity,
        primary_key=True
    )


class ModelWithAutoAssignedIdentity(BaseModel):
    id: int = pydantic.Field(1, primary_key=True)
    auto: int | None = pydantic.Field(None, auto_assign=True)


@pytest.mark.parametrize("Model", [
    ModelWithScalarIdentity,
    ModelWithCompositeIdentity,
    ModelWithNestedIdentity,
    ModelWithAutoAssignedIdentity
])
def test_model_has_key(Model: type[BaseModel]):
    assert hasattr(Model, '__key__')


@pytest.mark.parametrize("Model", [
    ModelWithScalarIdentity,
    ModelWithCompositeIdentity,
    ModelWithNestedIdentity,
    ModelWithAutoAssignedIdentity
])
def test_eq(Model: type[BaseModel]):
    obj1 = Model()
    obj2 = Model.parse_obj({
        k: v for k, v in obj1.__key__
    })
    assert obj1 == obj2


@pytest.mark.parametrize("Model", [
    ModelWithScalarIdentity,
    ModelWithCompositeIdentity,
    ModelWithNestedIdentity,
    ModelWithAutoAssignedIdentity
])
def test_neq(Model: type[BaseModel]):
    obj1 = Model()
    obj2 = Model(id=secrets.choice(range(0, 1000)))
    assert obj1 != obj2, f'{obj1.__key__} should not equal {obj2.__key__}'


@pytest.mark.parametrize("Model", [
    ModelWithScalarIdentity,
    ModelWithCompositeIdentity,
    ModelWithNestedIdentity,
    ModelWithAutoAssignedIdentity
])
def test_contains(Model: type[BaseModel]):
    objects = [
        Model(),
        Model(id=secrets.choice(range(0, 1000))),
        Model(id=secrets.choice(range(0, 1000))),
        Model(id=secrets.choice(range(0, 1000))),
    ]
    obj = Model()
    assert obj in objects
    assert len(list(filter(lambda x: x==obj, objects))) == 1


@pytest.mark.parametrize("Model", [
    ModelWithScalarIdentity,
    ModelWithCompositeIdentity,
    ModelWithNestedIdentity,
    ModelWithAutoAssignedIdentity
])
def test_not_contains(Model: type[BaseModel]):
    objects = [
        Model(id=secrets.choice(range(0, 1000))),
        Model(id=secrets.choice(range(0, 1000))),
        Model(id=secrets.choice(range(0, 1000))),
    ]
    obj = Model()
    assert obj not in objects
    assert len(list(filter(lambda x: x==obj, objects))) == 0


@pytest.mark.parametrize("Model", [
    ModelWithScalarIdentity,
    ModelWithCompositeIdentity,
    ModelWithNestedIdentity,
    ModelWithAutoAssignedIdentity
])
def test_list_remove(Model: type[BaseModel]):
    objects = [
        Model(),
        Model(),
        Model(id=secrets.choice(range(0, 1000))),
        Model(id=secrets.choice(range(0, 1000))),
        Model(id=secrets.choice(range(0, 1000))),
    ]
    objects.remove(Model())
    assert len(objects) == 4
    objects.remove(Model())
    assert len(objects) == 3


@pytest.mark.parametrize("Model", [
    ModelWithScalarIdentity,
    ModelWithCompositeIdentity,
    ModelWithNestedIdentity,
    ModelWithAutoAssignedIdentity
])
def test_set_types(Model: type[BaseModel]):
    objects = {
        Model(),
        Model(),
        Model(),
    }
    assert len(objects) == 1


def test_get_auto_assigned_field():
    instance = ModelWithAutoAssignedIdentity()
    assert hasattr(instance, '__surrogate__')
    assert instance.__surrogate__ is None
    instance.auto = 2
    assert instance.__surrogate__ == 2