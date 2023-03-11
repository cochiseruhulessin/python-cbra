# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import enum


class ClientAuthenticationMethod(str, enum.Enum):
    none        = 'none'
    post        = 'client_secret_post'
    basic       = 'client_secret_basic'
    jwt         = 'client_secret_jwt'
    private_key = 'private_key_jwt'
    tls         = 'tls_client_auth'
    self_signed = 'self_signed_tls_client_auth'