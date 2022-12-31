import asyncio
import logging

import uvicorn
from fastapi import FastAPI, Response, Request
from pydantic import BaseModel
from starlette import status
from starlette.responses import JSONResponse

from db.logger_db import Source, Level, Log
from db.models_management import get_or_create, get, create, create
from settings.settings import load_config

logger = logging.getLogger(__name__)
app = FastAPI()

config = load_config('.env')


class Secret(BaseModel):
    secret: str


class LogRequest(BaseModel):
    message: str
    token: str
    level: str


@app.post("/source")
async def get_or_create_source(secret: Secret, request: Request):
    source_url = f"{request.client.host}:{request.client.port}"
    if secret.secret == config.misc.secret:
        source = await get_or_create(Source, {'name': source_url}, 'token')
        return JSONResponse(content={"token": str(source)}, status_code=status.HTTP_202_ACCEPTED)
    else:
        return Response(status_code=status.HTTP_403_FORBIDDEN)


@app.post("/log")
async def store_log(data: LogRequest, request: Request):
    source = await get(Source, {"token": data.token})
    level = await get(Level, {"name": data.level.lower()})
    await create(Log, {"source_id": source.id, "level_id": level.id, "content": data.message})
    return Response(status_code=status.HTTP_202_ACCEPTED)


async def main():
    uvicorn.run(app)


if __name__ == "__main__":
    asyncio.run(main)
