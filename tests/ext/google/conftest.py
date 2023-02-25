# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import pytest

import google.oauth2.id_token
import google.auth.transport.requests
from google.auth.exceptions import DefaultCredentialsError
from google.cloud.datastore import Client
from cbra.ext.google.environ import GOOGLE_DATASTORE_NAMESPACE
from cbra.ext.google.environ import GOOGLE_SERVICE_PROJECT


@pytest.fixture(scope='session')
def google_id_token() -> str:
    audience = 'http://cbra.ext.google'
    try:
        request = google.auth.transport.requests.Request()
        return google.oauth2.id_token.fetch_id_token(request, audience) # type: ignore
    except DefaultCredentialsError:
        pytest.skip("Google default credentials not found")


@pytest.fixture(scope='session')
def client() -> Client:
    if not GOOGLE_SERVICE_PROJECT or not GOOGLE_DATASTORE_NAMESPACE:
        pytest.skip("Google not configured")
    return Client(
        project=GOOGLE_SERVICE_PROJECT,
        namespace=GOOGLE_DATASTORE_NAMESPACE
    )