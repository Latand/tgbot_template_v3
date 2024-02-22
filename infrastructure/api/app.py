import logging

import betterlogging as bl
import fastapi
from aiogram import Bot
from fastapi import FastAPI
from starlette.responses import JSONResponse

from tgbot.config import load_config, Config

app = FastAPI()
log_level = logging.INFO
bl.basic_colorized_config(level=log_level)
log = logging.getLogger(__name__)

config: Config = load_config(".env")
bot = Bot(token=config.tg_bot.token)


@app.post("/api")
async def webhook_endpoint(request: fastapi.Request):
    return JSONResponse(status_code=200, content={"status": "ok"})
