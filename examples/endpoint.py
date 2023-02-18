import uuid

import fastapi
import uvicorn

import cbra


class BookEndpoint(cbra.Endpoint):

    async def get(self, book_id: uuid.UUID):
        print(self.response)


app = fastapi.FastAPI(docs_url='/ui')
app.include_router(BookEndpoint.router, prefix='/books/{book_id}')


if __name__ == '__main__':
    uvicorn.run('__main__:app', reload=True) # type: ignore
