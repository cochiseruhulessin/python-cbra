# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.


class ICredential:
    """Used in conjunction with a :class:`IRequestPrincipal` implementation
    to establish the identity of a subject.
    """
    __module__: str = 'cbra.types'

    def is_verified(self) -> bool:
        """Some credentials are verified simply by existing."""
        return False