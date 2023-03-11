# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from canonical import DomainName


ALLOWED_DOMAINS: set[DomainName] = {
    DomainName('gmail.com'),
    DomainName('outlook.com'),
    DomainName('hotmail.com'),
    DomainName('live.com'),
    DomainName('myyahoo.com'),
    DomainName('yahoo.com'),
    DomainName('rocketmail.com'),
    DomainName('icloud.com'),
    DomainName('pm.me'),
    DomainName('protonmail.com')
}

DEFAULT_SIGNING_KEY: str = 'oauth2.sig'