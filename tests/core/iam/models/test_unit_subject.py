# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import datetime

import pytest

from canonical import EmailAddress
from headless.ext.oauth2.models import SubjectIdentifier

from cbra.core.iam.models import Subject


@pytest.mark.parametrize("principal", [
    EmailAddress('cochiseruhulessin@gmail.com'),
    SubjectIdentifier(iss="https://accounts.google.com", sub='123')
])
def test_can_not_add_duplicate_principals(
    principal: EmailAddress | SubjectIdentifier
):
    subject = Subject()
    subject.add_principal(principal, datetime.datetime.now())
    with pytest.raises(ValueError):
        subject.add_principal(principal, datetime.datetime.now())