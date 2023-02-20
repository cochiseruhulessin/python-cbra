# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import cbra.core as cbra


class AuthenticatedEndpoint(cbra.Endpoint):

    async def get(self) -> dict[str, bool | str]:
        return {
            'remote_host': str(self.ctx.remote_host),
            'is_authenticated': self.ctx.is_authenticated()
        }


app: cbra.Application = cbra.Application()
app.inject('TRUSTED_AUTHORIZATION_SERVERS', ['https://accounts.google.com'])
app.add(AuthenticatedEndpoint)


if __name__ == '__main__':
    import uvicorn
    uvicorn.run('__main__:app', reload=True)
