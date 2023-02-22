# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import datetime
import hashlib
from typing import Any

import pydantic


class IHashable:
    __module__: str = 'cbra.types'

    def digest(self) -> bytes:
        raise NotImplementedError

    @staticmethod
    def _hash(obj: Any) -> bytes:
        h = hashlib.sha3_256()
        if isinstance(obj, IHashable):
            h.update(obj.digest())
        elif isinstance(obj, str):
            h.update(str.encode(obj, encoding='utf-8'))
        elif isinstance(obj, int):
            h.update(
                int.to_bytes(obj, (obj.bit_length() + 7) // 8, 'big')
            )
        elif isinstance(obj, dict):
            for key in sorted(obj.keys()): # type: ignore
                assert isinstance(key, str)
                h.update(IHashable._hash(key))
                h.update(IHashable._hash(obj[key]))
        elif isinstance(obj, list):
            for item in obj: # type: ignore
                h.update(IHashable._hash(item))
        elif isinstance(obj, datetime.datetime):
            h.update(IHashable._hash(obj.isoformat()))
        elif isinstance(obj, pydantic.BaseModel):
            for k in obj.__fields__.keys():
                h.update(str.encode(k, 'ascii'))
                h.update(IHashable._hash(getattr(obj, 'k')))
        elif obj is None:
            pass
        else:
            raise TypeError(f'Unhashable type: {repr(obj)}')
        return h.digest()