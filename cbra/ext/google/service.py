# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Any

from cbra.core import Application
from cbra.core.utils import parent_signature
from .aortaendpoint import AortaEndpoint
from .environ import GOOGLE_DATASTORE_NAMESPACE
from .environ import GOOGLE_SERVICE_PROJECT


class Service(Application):
    __module__: str = 'cbra.ext.google'

    @parent_signature(Application.__init__)
    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        if GOOGLE_SERVICE_PROJECT and GOOGLE_DATASTORE_NAMESPACE:
            from google.cloud.datastore import Client
            self.inject(
                name='GoogleDatastoreClient',
                value=Client(
                    project=GOOGLE_SERVICE_PROJECT,
                    namespace=GOOGLE_DATASTORE_NAMESPACE
                )
            )
            self.container.provide('SubjectResolver', {
                'qualname': 'cbra.ext.google.DatastoreSubjectResolver'
            })
            self.container.provide('SubjectRepository', {
                'qualname': 'cbra.ext.google.DatastoreSubjectRepository'
            })
        self.add(AortaEndpoint, path="/.well-known/aorta")