# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
"""

.. _guides-picqer:

===================================
Building an application with Picqer
===================================


Settings
========

.. setting:: PICQER_WEBHOOK_SECRET

    Default: `None`

    The secret used to verify incoming webhooks from Picqer. This is the
    default secret used by :class:`~cbra.ext.picqer.PicqerWebhookEndpoint`.
"""
from cbra.core.conf import settings

from .picqerwebhookendpoint import PicqerWebhookEndpoint
from .webhooksecret import WebhookSecret
from . import v1


settings.register('PICQER_WEBHOOK_SECRET', None)


__all__: list[str] = [
    'v1',
    'PicqerWebhookEndpoint',
    'WebhookSecret',
]