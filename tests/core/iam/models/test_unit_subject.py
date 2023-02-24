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
    assert old == new
    assert new.trust


def test_trusted_principal_overwrites_untrusted():
    now = datetime.now(timezone.utc)
    iss = 'https://python-cbra.dev.cochise.io'
    email = EmailAddress('foo@bar.baz')
    subject = Subject(kind='User', uid=1, created=now, seen=now)
    subject.add_principal(iss, email, now, False)
    old = list(subject.principals)[0]
    assert not old.trust

    subject.add_principal(iss, email, now, True)
    new = list(subject.principals)[0]
    assert old == new
    assert new.trust


def test_has_principal():
    now = datetime.now(timezone.utc)
    iss = 'https://python-cbra.dev.cochise.io'
    email = EmailAddress('foo@bar.baz')
    subject = Subject(kind='User', uid=1, created=now, seen=now)
    subject.add_principal(iss, email, now, False)
    assert subject.has_principal(email)


def test_add_email_from_different_issuers():
    now = datetime.now(timezone.utc)
    i1 = "https://accounts.google.com"
    i2 = "https://outlook.microsoft.com"
    email = EmailAddress('foo@bar.baz')
    subject = Subject(kind='User', uid=1, created=now, seen=now)
    subject.add_principal(i1, email, now, False)
    subject.add_principal(i2, email, now, False)
    assert len(subject.principals) == 1


def test_override_email_with_trusted_issuer():
    now = datetime.now(timezone.utc)
    i1 = "https://accounts.google.com"
    i2 = "https://outlook.microsoft.com"
    email = EmailAddress('foo@bar.baz')
    subject = Subject(kind='User', uid=1, created=now, seen=now)
    subject.add_principal(i1, email, now, False)
    subject.add_principal(i2, email, now, True)
    assert len(subject.principals) == 1
    assert subject.principals.pop().spec.iss == i2