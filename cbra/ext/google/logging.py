# Copyright (C) 2021-2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import collections.abc
import json
import logging
from typing import Any


class JSONFormatter(logging.Formatter):
    __module__: str = 'cbra.ext.google.logging'

    def format(self, record: logging.LogRecord) -> str:
        super().format(record)
        params: dict[str, Any] = {
            'message': record.msg
        }
        if isinstance(record.msg, collections.abc.Mapping):
            params.update(record.msg)
        else:
            params['message'] = super().formatMessage(record)
        if record.exc_info:
            assert record.exc_info[0] is not None
            params['exception'] = {
                'type': f'{record.exc_info[0].__module__}.{record.exc_info[0].__name__}',
                'stack': self.formatException(record.exc_info)
            }
        return json.dumps(params)