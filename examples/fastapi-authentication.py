# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import fastapi
import uvicorn

import cbra.core as cbra
from cbra.core.iam import AuthorizationContextFactory
from cbra.types import Principal


app: cbra.Application = cbra.Application()


@app.get('/')
async def f(
    request: fastapi.Request,
    factory: AuthorizationContextFactory = fastapi.Depends(),
    principal: Principal = fastapi.Depends(Principal.fromrequest)
):
    ctx = await factory.authenticate(request, principal)
    return {
        'remote_host': ctx.remote_host,
        'is_authenticated': ctx.is_authenticated()
    }


if __name__ == '__main__':
    uvicorn.run(app) # type: ignore