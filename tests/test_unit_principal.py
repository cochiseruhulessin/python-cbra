# Copyright (C) 2021-2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import pytest

from cbra.types import NullRequestPrincipal
from cbra.types import RequestPrincipal
from cbra.types import OIDCRequestPrincipal
from cbra.types import RFC9068RequestPrincipal


def test_parse_bearer_oidc():
    token = (
        'eyJ0eXAiOiJKV1QiLCJhbGciOiJFUzI1NiIsImtpZCI6IjgwNDFiM2VmYWRlYm'
        'VlMjNhOWY5MTZhZjU0MDBhYmJlIn0.eyJhdWQiOiJodHRwczovL2xvY2FsaG9z'
        'dDo4MDAwIiwiYXpwIjoiY2xpZW50X2lkIiwiZW1haWwiOiJ1c2VyQGV4YW1wbG'
        'UuY29tIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsImV4cCI6MTY3Njg5MTI5Miwi'
        'aWF0IjoxNjc2ODg3NjkyLCJpc3MiOiJodHRwczovL2NicmEiLCJzdWIiOiIxMj'
        'MifQ.R0KqeCRFNc4dRJCf6lBkH6AviYNa-t36xHkQD1vkG5eUaFJyB2OUjvQVS'
        'jP-QfHmoRUj5yV8zaBOpz1rl6fXHw'
    )
    principal = RequestPrincipal.parse_obj({
        'headers': {'Authorization': f'Bearer {token}'}
    })
    assert isinstance(principal.__root__, OIDCRequestPrincipal)


def test_parse_bearer_rfc9068():
    token = (
        'eyJ0eXAiOiJhdCtqd3QiLCJhbGciOiJFUzI1NiIsImtpZCI6IjgwNDFiM2VmYWRl'
        'YmVlMjNhOWY5MTZhZjU0MDBhYmJlIn0.eyJpc3MiOiJodHRwczovL2FjY291bnRz'
        'LndlYmlkZW50aXR5LmlkIiwic3ViIjoiY2xpZW50X2lkIiwiYXVkIjoiaHR0cHM6'
        'Ly9sb2NhbGhvc3Q6ODAwMCIsImV4cCI6MTY3Njg4ODIzMSwibmJmIjoxNjc2ODg3'
        'OTMxLCJpYXQiOjE2NzY4ODc5MzEsImp0aSI6IkJleGE1RzlZX05RZW83SXd0MU4z'
        'N0l1WENiWUkxQlo1IiwiY2xpZW50X2lkIjoiY2xpZW50X2lkIn0.XI18HDgpu8YI'
        'GHASGuTkOb2hnI9lDBZHNlFl-Tsl7fXeHbyc7IMvw1o7h4MeEFEubVPeTq-FHZzo'
        'aX0Wea6QWQ'
    )
    principal = RequestPrincipal.parse_obj({
        'headers': {'Authorization': f'Bearer {token}'}
    })
    assert isinstance(principal.__root__, RFC9068RequestPrincipal)



@pytest.mark.parametrize("value", [
    'Bearer '
    'aeyJ0eXAiOiJhdCtqd3QiLCJhbGciOiJFUzI1NiIsImtpZCI6IjgwNDFiM2VmYWRl'
    'YmVlMjNhOWY5MTZhZjU0MDBhYmJlIn0.eyJpc3MiOiJodHRwczovL2FjY291bnRz'
    'LndlYmlkZW50aXR5LmlkIiwic3ViIjoiY2xpZW50X2lkIiwiYXVkIjoiaHR0cHM6'
    'Ly9sb2NhbGhvc3Q6ODAwMCIsImV4cCI6MTY3Njg4ODIzMSwibmJmIjoxNjc2ODg3'
    'OTMxLCJpYXQiOjE2NzY4ODc5MzEsImp0aSI6IkJleGE1RzlZX05RZW83SXd0MU4z'
    'N0l1WENiWUkxQlo1IiwiY2xpZW50X2lkIjoiY2xpZW50X2lkIn0.XI18HDgpu8YI'
    'GHASGuTkOb2hnI9lDBZHNlFl-Tsl7fXeHbyc7IMvw1o7h4MeEFEubVPeTq-FHZzo'
    'aX0Wea6QWQ',
    'Bearer foo',
    'Foo',
])
def test_parse_bearer_malformed_becomes_nullrequestprincipal(value: str):
    token = (
    )
    principal = RequestPrincipal.parse_obj({
        'headers': {'Authorization': token}
    })
    assert isinstance(principal.__root__, NullRequestPrincipal)


def test_bearer_untyped_jwt_is_nullrequestprincipal():
    token = (
        'eyJhbGciOiJFUzI1NiIsImtpZCI6IjgwNDFiM2VmYWRlYmVlMjNhOWY5MTZhZjU0'
        'MDBhYmJlIn0.eyJpc3MiOiJodHRwczovL2FjY291bnRzLndlYmlkZW50aXR5Lmlk'
        'Iiwic3ViIjoiY2xpZW50X2lkIiwiYXVkIjoiaHR0cHM6Ly9sb2NhbGhvc3Q6ODAw'
        'MCIsImV4cCI6MTY3Njg4ODIzMSwibmJmIjoxNjc2ODg3OTMxLCJpYXQiOjE2NzY4'
        'ODc5MzEsImp0aSI6IkJleGE1RzlZX05RZW83SXd0MU4zN0l1WENiWUkxQlo1Iiwi'
        'Y2xpZW50X2lkIjoiY2xpZW50X2lkIn0.P54GYkelEWnQGWgg8qP_CMZaOI_rlWEP'
        'wU1dh5WkZRL5Dx4jly94_wO6HTW4If1VzPKWFJiDNPNUqDr650iq_Q'
    )
    principal = RequestPrincipal.parse_obj({
        'headers': {'Authorization': f'Bearer {token}'}
    })
    assert isinstance(principal.__root__, NullRequestPrincipal)


def test_bearer_unaccepted_jwt_is_nullrequestprincipal():
    token = (
        'eyJhbGciOiJFUzI1NiIsInR5cCI6ImZvbyIsImtpZCI6IjgwNDFiM2VmYWRlYmVl'
        'MjNhOWY5MTZhZjU0MDBhYmJlIn0.eyJpc3MiOiJodHRwczovL2FjY291bnRzLndl'
        'YmlkZW50aXR5LmlkIiwic3ViIjoiY2xpZW50X2lkIiwiYXVkIjoiaHR0cHM6Ly9s'
        'b2NhbGhvc3Q6ODAwMCIsImV4cCI6MTY3Njg4ODIzMSwibmJmIjoxNjc2ODg3OTMx'
        'LCJpYXQiOjE2NzY4ODc5MzEsImp0aSI6IkJleGE1RzlZX05RZW83SXd0MU4zN0l1'
        'WENiWUkxQlo1IiwiY2xpZW50X2lkIjoiY2xpZW50X2lkIn0.U9iSF3Kluw1gBFAL'
        'IdEJVwwGCHO_DS5JZlqs_8ynA8srOjY00hYB2cWLeJ6RIwcNRE2IPsSkwbmP6kGD'
        '6ym0wA'
    )
    principal = RequestPrincipal.parse_obj({
        'headers': {'Authorization': f'Bearer {token}'}
    })
    assert isinstance(principal.__root__, NullRequestPrincipal)