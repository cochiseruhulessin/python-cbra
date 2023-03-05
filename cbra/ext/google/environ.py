# Copyright (C) 2020-2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import os


__all__: list[str] = [
    'GOOGLE_DATASTORE_NAMESPACE',
    'GOOGLE_HOST_PROJECT',
    'GOOGLE_SERVICE_PROJECT',
]


GOOGLE_DATASTORE_NAMESPACE: str | None = os.environ.get('GOOGLE_DATASTORE_NAMESPACE')

GOOGLE_HOST_PROJECT: str | None = os.environ.get('GOOGLE_HOST_PROJECT')

GOOGLE_SERVICE_PROJECT: str | None = os.environ.get('GOOGLE_SERVICE_PROJECT')