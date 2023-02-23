# Copyright (C) 2021-2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import urllib.parse
from typing import Any

import pydantic
import pytest

from cbra.ext.oauth2.types import RedirectURI


@pytest.mark.parametrize("value", [
    "https://google.com/callback",
    "http://127.0.0.1/callback",
    "http://127.0.0.1:8000/callback",
    "http://[::1]/callback",
    "http://[::1]:8000/callback",
    "https://google.com/",
    "http://127.0.0.1/",
    "http://127.0.0.1:8000/",
    "http://[::1]/",
    "http://[::1]:8000/",
])
def test_valid_values(value: Any):
    for validate in RedirectURI.__get_validators__():
        validate(value)


@pytest.mark.parametrize("value", [
    "invalid",
    None,
    'a' * 2049,
    'http://www.google.com/callback',
    'http://localhost:8000/callback',
    'https://localhost:8000/callback',
    'https://localhost:8000/callback?foo=bar',
    'https://localhost:8000/callback#fragment',
    'http://1.1.1.1/callback',
])
def test_invalid_values(value: Any):
    with pytest.raises((pydantic.errors.PydanticTypeError, ValueError)):
        for validate in RedirectURI.__get_validators__():
            validate(value)


def test_cast_to_string():
    url = RedirectURI(urllib.parse.urlparse('https://www.google.com'))
    assert str(url) == 'https://www.google.com'


def test_create_redirect_uri():
    url = RedirectURI(urllib.parse.urlparse('https://www.google.com'))
    p = urllib.parse.urlparse(url.redirect(foo='bar'))
    q = dict(urllib.parse.parse_qsl(p.query))
    assert 'foo' in q
    assert q.get('foo') == 'bar'