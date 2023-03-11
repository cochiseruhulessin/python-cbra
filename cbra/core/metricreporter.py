# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import logging
from typing import Any


class MetricReporter:
    __module__: str = 'cbra.core'
    group: str | None = None
    logger: logging.Logger = logging.getLogger('cbra.endpoint')

    def __init__(self, group: str | None = None) -> None:
        self.group = group

    def report(
        self,
        name: str,
        data: dict[str, Any],
        message: str | None = None,
        *,
        version: str = 'v1'
    ):
        if self.group:
            version = f'{self.group}/{version}'
        self.logger.info({
            'message': message or f'Metric reported: {version}/{name}',
            'apiVersion': version,
            'kind': name,
            'type': 'cochise.io/metric',
            'data': data
        })