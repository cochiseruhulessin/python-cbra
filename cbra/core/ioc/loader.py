# Copyright (C) 2016-2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
"""Declares functions to import dependencies."""
import importlib
from typing import Any


BUILTINS = __builtins__


def import_module(qualname: str, fail_silent: bool = False) -> Any:
    """Import a Python module using its qualified name `qualname`."""
    try:
        return importlib.import_module(qualname)
    except ImportError:
        if not fail_silent:
            raise
        return None


def import_builtin(qualname: str, fail_silent: bool = False) -> Any:
    """Import a builtin type."""
    try:
        return BUILTINS[qualname]
    except KeyError:
        if not fail_silent:
            raise ImportError(qualname) # pylint: disable=W0707

        return None


def import_symbol(qualname: str, fail_silent: bool = False) -> Any:
    """Import a symbol. The symbol may be one of the following and
    are considered in this order:

    -   A module;
    -   A class, function or variable in a module;
    -   A builtin type, or a member of a builtin type.
    """
    parts = qualname.rsplit('.', 1)
    if len(parts) == 1:
        result = import_module(parts[0], True) or import_builtin(parts[0], True)
        if result is None and not fail_silent:
            raise ImportError(qualname) # pylint: disable=W0707

        return result

    namespace, name = parts
    parent: Any | None = None
    if namespace.count('.') == 0: # Module or builtin type
        parent = import_symbol(namespace, True)
    else:
        parent = import_module(namespace, True)\
            or import_symbol(namespace, True)

    if parent is None and not fail_silent:
        raise ImportError(qualname) # pylint: disable=W0707

    try:
        return getattr(parent, name)
    except AttributeError:
        if not fail_silent:
            raise ImportError(qualname) # pylint: disable=W0707

        return None
