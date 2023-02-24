# Copyright (C) 2021-2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from datetime import datetime
from datetime import timezone

import pytest
from canonical import EmailAddress

from cbra.core.iam.models import Subject


def test_trusted_principal_does_not_get_overwritten_by_untrusted():
    now = datetime.now(timezone.utc)
    iss = 'https://python-cbra.dev.cochise.io'
    email = EmailAddress('foo@bar.baz')
    subject = Subject(kind='User', uid=1, created=now, seen=now)
    subject.add_principal(iss, email, now, True)
    old = list(subject.principals)[0]
    assert old.trust

    subject.add_principal(iss, email, now, False)
    new = list(subject.principals)[0]
    assert new.trust