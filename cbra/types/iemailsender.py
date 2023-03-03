# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from types import EllipsisType
from typing import Any
from typing import Protocol


class IEmailSender(Protocol):
    """Knows how to send (signed) email to one or many recipients, using
    pre-rendered strings or templates.
    """
    __module__: str = 'cbra.types'

    async def send(
        self,
        sender: str | EllipsisType,
        recipients: list[str],
        subject: str,
        content: dict[str, str],
        headers: dict[str, Any] | None = None,
        cc: list[str] | None = None,
        bcc: list[str] | None = None
    ) -> None:
        """Send an email message to the specified recipients.
        
        Args:
            sender: email address that is the sender of the email. May be
                an ellipsis to indicate that a default sender must be used.
            recipients: the list of recipients.

        Returns:
            None

        Raises:
            :class:`EmailServiceNotAvailable`
        """
        ...

    async def send_template(
        self,
        sender: str | EllipsisType,
        recipients: list[str],
        subject: str,
        templates: dict[str, str],
        context: dict[str, Any] | None = None,
        headers: dict[str, Any] | None = None,
        cc: list[str] | None = None,
        bcc: list[str] | None = None
    ) -> None:
        ...

    async def get_default_sender(self) -> str:
        ...