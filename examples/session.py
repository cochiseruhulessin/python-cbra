# Copyright (C) 2021-2023 Cochise Ruhulessin
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
from cbra.core.sessions import RequestSession


app: cbra.Application = cbra.Application()


@app.get('/')
async def f(
    request: fastapi.Request,
    response: fastapi.Response,
    session: RequestSession = fastapi.Depends()
):
    await session
    session.set('sub', 'foo')
    await session.add_to_response(response)
    return session.data.dict()

if __name__ == '__main__':
    uvicorn.run('__main__:app', reload=True) # type: ignore