import json
import logging.handlers

import requests


class CustomHTTPHandler(logging.Handler):
    def __init__(self, host, method="POST"):
        super().__init__()
        self.host = host
        self.method = method
        response = requests.post(f"http://{self.host}/source",
                                 data=json.dumps({"secret": "fk1F17uZDTIv7iAMh2Jtqew0K1jKXHTp"}))
        self.token = eval(response.text)["token"]

    def emit(self, record: logging.LogRecord) -> None:
        level = record.levelname.lower()
        message = {"token": self.token, "level": level, "message": record.msg, "created": record.created,
                   "exception_info": record.exc_info, "exception_text": record.exc_text, "filename": record.filename,
                   "function_name": record.funcName, "line_of_code": record.lineno, "module": record.module,
                   "logger_name": record.name, "path": record.pathname, "process": record.process,
                   "process_name": record.processName}

        requests.post(f"http://{self.host}/log",
                      data=json.dumps(message))


log_config = {
    "version": 1,
    "handlers": {
        "server": {
            "()": CustomHTTPHandler,
            "level": "DEBUG",
            "host": "127.0.01:8002",
            "method": "POST"
        },
    },
    "loggers": {
        "root": {
            "handlers": ["server"],
            "level": "DEBUG",
        },
    },
}
