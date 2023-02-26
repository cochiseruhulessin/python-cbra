# Copyright (C) 2021-2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import itertools
import re
from typing import Any

import inflect

from .createaction import CreateAction
from .customaction import CustomAction
from .deleteaction import DeleteAction
from .listaction import ListAction
from .replaceaction import ReplaceAction
from .resourceaction import ResourceAction
from .retrieveaction import RetrieveAction
from .updateaction import UpdateAction


engine: inflect.engine = inflect.engine()


class ResourceType(type):
    __module__: str = 'cbra.core'
    actions: dict[str, type[ResourceAction]] = {
        'create'    : CreateAction,
        'destroy'   : DeleteAction,
        'list'      : ListAction,
        'replace'   : ReplaceAction,
        'retrieve'  : RetrieveAction,
        'update'    : UpdateAction,
        #'notify',
    }

    def __new__(
        cls,
        name: str,
        bases: tuple[type, ...],
        namespace: dict[str, Any],
        **params: Any
    ):
        actions: list[ResourceAction] = []
        is_abstract = namespace.pop('__abstract__', False)
        if not is_abstract:
            Model = params.get('model', None)
            if Model is None:
                raise TypeError('The `model` class argument is required.')

            # Collect actions and convert them to ResourceAction instances, if
            # necessary. First inspect the bases for known actions, and then
            # the namespace of the class we're creating.
            parent_actions: dict[str, ResourceAction] = {}
            collection_actions: set[str] = set()
            detail_actions: set[str] = set()

            for action_name, base in itertools.product(cls.actions, bases):
                handler = getattr(base, action_name, None)
                if handler is None:
                    continue
                parent_actions[action_name] = handler

            for action_name in cls.actions:
                action = namespace.get(action_name) or parent_actions.get(action_name)
                if action is None:
                    continue
                if not isinstance(action, ResourceAction):
                    action = cls.actions[action_name].fromfunc(name, action)
                if action.is_detail(): detail_actions.add(action.method)
                if not action.is_detail(): collection_actions.add(action.method)
                actions.append(action)

            # Get local non-default actions
            for func in namespace.values():
                if not hasattr(func, 'action'):
                    continue
                action = CustomAction.fromfunc(name, func)
                if action.is_detail(): detail_actions.add(action.method)
                if not action.is_detail(): collection_actions.add(action.method)
                actions.append(action)

            # Update the namespace with the actions and resource name.
            namespace.update({
                '__actions__': actions,
                'resource_name': Model.__name__,
            })
            
            # Some naming stuff.
            verbose_name = namespace.get('verbose_name') or namespace['resource_name']
            verbose_name_plural = namespace.get('verbose_name_plural')\
                or engine.plural_noun(verbose_name)
            namespace.update({
                'verbose_name': verbose_name,
                'verbose_name_plural': verbose_name_plural
            })

            # Construct the path name, if not provided, using the 
            # resource name.
            path_name: Any = namespace.setdefault(
                'path_name',
                engine.plural_noun(str.lower(Model.__name__))
            )
            if not isinstance(path_name, str)\
            or not re.match('[a-zA-Z0-9]', path_name[0]):
                raise TypeError(
                    f'{name}.path_name must be a string consisting of '
                    'alphanumeric characters.'
                )

        Resource = super().__new__(cls, name, bases, namespace, **params)
        if not is_abstract and actions:
            for action in actions:
                action.add_to_class(Resource) # type: ignore
        return Resource