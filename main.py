import asyncio
import datetime
import logging
from typing import Optional

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
    message: Optional[str]
    token: str
    level: str
    path: Optional[str]
    filename: Optional[str]
    module: Optional[str]
    logger_name: Optional[str]
    function_name: Optional[str]
    line_of_code: Optional[int]
    process: Optional[str]
    process_name: Optional[str]
    exception_info: Optional[str]
    exception_text: Optional[str]
    created: Optional[int]


@app.post("/source")
async def get_or_create_source(secret: Secret, request: Request):
    source_url = f"{request.client.host}:{request.client.port}"
    if secret.secret == config.misc.secret:
        source = await get_or_create(Source, {'name': source_url}, 'token')
        return JSONResponse(content={"token": str(source)}, status_code=status.HTTP_202_ACCEPTED)
    else:
        return Response(status_code=status.HTTP_403_FORBIDDEN)


@app.post("/log")
async def store_log(data: LogRequest):
    source = await get(Source, {"token": data.token})
    level = await get(Level, {"name": data.level.lower()})
    try:
        await create(Log, {"source_id": source.id, "level_id": level.id, "message": data.message,
                           "file_path": data.path, "filename": data.filename, "module": data.module,
                           "logger_name": data.logger_name, "function_name": data.function_name,
                           "line_of_code": data.line_of_code, "process": data.process,
                           "process_name": data.process_name, "exception_info": data.exception_info,
                           "exception_text": data.exception_text,
                           "created_at": datetime.datetime.fromtimestamp(data.created)})
        return Response(status_code=status.HTTP_202_ACCEPTED)
    except Exception as exc:
        print(exc.args)
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


async def main():
    uvicorn.run(app)


if __name__ == "__main__":
    asyncio.run(main)
