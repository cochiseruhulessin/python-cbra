# Copyright (C) 2021-2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from datetime import datetime
from datetime import timedelta
from datetime import timezone
from typing import Any

import pytest
from headless.ext.oauth2.types import GrantType

from cbra.ext.oauth2.models import RefreshToken
from cbra.ext.oauth2.types import RefreshTokenPolicyType
from cbra.ext.oauth2.types import RefreshTokenType
from cbra.ext.oauth2.types import RefreshTokenStatus



@pytest.fixture
def params() -> dict[str, Any]:
    now = datetime.now(timezone.utc)
    return {
        'created': now,
        'client_id': 'self',
        'granted': now,
        'grant_id': 0,
        'grant_type': GrantType.authorization_code,
        'ppid': 1000,
        'scope': {'email', 'openid', 'profile'},
        'sector_identifier': 'example.com',
        'status': RefreshTokenStatus.active,
        'sub': 1,
        'token': RefreshTokenType('foo')
    }


def test_refresh_rolling(
    params: dict[str, Any]
):
    ttl = 86400
    t1 = RefreshToken.parse_obj({
        **params,
        'renew': RefreshTokenPolicyType.rolling,
        'ttl': ttl
    })
    t2 = t1.refresh()
    assert t1.token != t2.token
    assert t2.expires == (t2.created + timedelta(seconds=ttl))
    assert not t1.is_active()


def test_refresh_static(
    params: dict[str, Any]
):
    ttl = 86400
    t1 = RefreshToken.parse_obj({
        **params,
        'renew': RefreshTokenPolicyType.static,
        'ttl': ttl
    })
    t2 = t1.refresh()
    assert t1.token != t2.token
    assert t2.expires == (t1.granted + timedelta(seconds=ttl))
    assert not t1.is_active()


def test_can_use(
    params: dict[str, Any]
):
    ttl = 86400
    t1 = RefreshToken.parse_obj({
        **params,
        'renew': RefreshTokenPolicyType.static,
        'ttl': ttl
    })
    assert t1.can_use({'openid'})
    assert not t1.can_use({'foo'})