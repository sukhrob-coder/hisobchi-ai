import asyncio
import logging

from aiogram import Bot, Dispatcher

from app.core.config import settings
from .handlers import router

logging.basicConfig(level=logging.INFO)

async def main():
    bot = Bot(token=settings.BOT_TOKEN)
    dp = Dispatcher()

    dp.include_router(router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Bot stopped!")
