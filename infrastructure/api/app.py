import logging

import betterlogging as bl
import fastapi
from fastapi import FastAPI
from starlette.responses import JSONResponse

app = FastAPI()
log_level = logging.INFO
bl.basic_colorized_config(level=log_level)
log = logging.getLogger(__name__)


@app.post("/api")
async def webhook_endpoint(request: fastapi.Request):
    return JSONResponse(status_code=200, content={"status": "ok"})
