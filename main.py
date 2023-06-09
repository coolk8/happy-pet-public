from pathlib import Path
import asyncio
import logging
import openai
from motor.motor_tornado import MotorClient
import backoff

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage, Redis
from pyi18n import PyI18n

from config_dataclass.config import Config, load_config
from handlers import intro_handlers

logging.basicConfig(level=logging.DEBUG,
                    format="%(asctime)s %(levelname)s %(message)s")
logging.getLogger('backoff').addHandler(logging.StreamHandler())

async def main() -> None:
    config: Config = load_config()
    redis: Redis = Redis(host=config.redis.host, port=config.redis.port, db=config.redis.db, password=config.redis.password)
    storage: RedisStorage = RedisStorage(redis=redis)
    openai.api_key = config.openai_service.api_key


    bot: Bot = Bot(token=config.tg.token)
    client = MotorClient(config.mongodb.url)
    db = client['bot']
    users_collection = db['users']

    dp: Dispatcher = Dispatcher(storage=storage, 
                                users_collection=users_collection)

    dp.include_router(router=intro_handlers.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
