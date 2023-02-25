# Copyright (C) 2022 Cochise Ruhulessin # type: ignore
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import pytest
import pytest_asyncio
from headless.core import httpx

import cbra.core as cbra
from cbra import types
from cbra.ext.picqer import PicqerWebhookEndpoint
from cbra.ext.picqer import WebhookSecret

VALID_SIGNATURE: str = '3TMYo2hAFdgQ9bF4MJZ4/dnELdJv5ucJPRAEnoE3Qxk='

VALID_BODY: str = (
    '{"idhook":14381,"name":"created.picklists.picqer.localhost:8000","event":'
    '"picklists.created","event_triggered_at":"2023-02-25 04:34:57","data":{"i'
    'dpicklist":81146972,"picklistid":"P2023-1289","idcustomer":40454718,"idor'
    'der":118330126,"idreturn":null,"idwarehouse":6790,"idtemplate":6375,"idsh'
    'ippingprovider_profile":null,"deliveryname":"ACME","deliverycontact":"Wil'
    'liam Jobs","deliveryaddress":"Renwick Drive 70","deliveryaddress2":"","de'
    'liveryzipcode":"19108","deliverycity":"Philadelphia","deliveryregion":"PA'
    '","deliverycountry":"US","telephone":null,"emailaddress":"n.defeber@molan'
    'o.nl","reference":null,"assigned_to_iduser":null,"invoiced":false,"urgent'
    '":false,"preferred_delivery_date":null,"status":"new","totalproducts":10,'
    '"totalpicked":0,"snoozed_until":null,"closed_by_iduser":null,"closed_at":'
    'null,"created":"2023-02-25 04:34:56","updated":"2023-02-25 04:34:57","pro'
    'ducts":[{"idpicklist_product":190774372,"idproduct":23286044,"idorder_pro'
    'duct":295834751,"idreturn_product_replacement":null,"idvatgroup":14586,"p'
    'roductcode":"XXXBAZ","name":"Test Product Baz","remarks":"","amount":5,"a'
    'mountpicked":0,"amount_picked":0,"price":1,"weight":0,"stocklocation":nul'
    'l,"stock_location":null,"partof_idpicklist_product":null,"has_parts":fals'
    'e},{"idpicklist_product":190774373,"idproduct":23286043,"idorder_product"'
    ':295834752,"idreturn_product_replacement":null,"idvatgroup":14586,"produc'
    'tcode":"XXXBAR","name":"Test Product Bar","remarks":"","amount":5,"amount'
    'picked":0,"amount_picked":0,"price":1,"weight":0,"stocklocation":null,"st'
    'ock_location":null,"partof_idpicklist_product":null,"has_parts":false}],"'
    'comment_count":0}}'
)



@pytest.fixture
def app() -> cbra.Application:
    return cbra.Application()


@pytest_asyncio.fixture # type: ignore
async def client(app: cbra.Application):
    class T(PicqerWebhookEndpoint):
        async def get_webhook_secret(self) -> types.Verifier:
            return WebhookSecret('test')

    app.add(T, path='/')
    async with httpx.Client(base_url='http://cbra.ext.google', app=app) as client:
        yield client


@pytest.mark.asyncio
async def test_no_signature_is_refused(
    client: httpx.Client
):
    response = await client.post(
        url='/',
        content=VALID_BODY,
        headers={'Content-Type': "application/json"}
    )
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_invalid_signature_is_refused(
    client: httpx.Client
):
    response = await client.post(
        url='/',
        content=VALID_BODY,
        headers={
            'Content-Type': "application/json",
            'X-Picqer-Signature': 'aa'
        }
    )
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_valid_signature_is_accepted(
    client: httpx.Client
):
    response = await client.post(
        url='/',
        content=VALID_BODY,
        headers={
            'Content-Type': "application/json",
            'X-Picqer-Signature': VALID_SIGNATURE
        }
    )
    assert response.status_code == 200