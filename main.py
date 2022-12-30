import asyncio
import logging

import uvicorn
from fastapi import FastAPI, Response, Request, Depends
from pydantic import BaseModel, json
from starlette import status
from starlette.responses import JSONResponse

from db.db_setup import global_init
from db.logger_db import Source
from settings.settings import load_config


logger = logging.getLogger(__name__)
app = FastAPI()

config = load_config('.env')


class Secret(BaseModel):
    secret: str


class Log(BaseModel):
    data: str
    token: str


@app.post("/source")
async def get_or_create_source(secret: Secret, request: Request):
    source_url = f"{request.client.host}:{request.client.port}"
    if secret.secret == config.misc.secret:
        source = await Source.get_or_create({'name': source_url})
        return JSONResponse(content={"token": str(source.token)}, status_code=status.HTTP_202_ACCEPTED)
    else:
        return Response(status_code=status.HTTP_403_FORBIDDEN)


@app.post("/log")
async def store_log(data: Log, request: Request):
    token = data.token
    source = await Source.get({"token": token})
    logger.info(source)
    print(source.name)
    return JSONResponse(status_code=status.HTTP_202_ACCEPTED)


async def main():
    global_init(config)
    uvicorn.run(app)


if __name__ == "__main__":
    asyncio.run(main)
