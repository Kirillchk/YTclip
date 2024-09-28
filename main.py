import asyncio
import logging
import config
from aiogram import Bot, Dispatcher
from apps.handler import rout
from apps.VisualInterface import set_bot_commands


bot = Bot(token=config.TOKEN)
dp = Dispatcher()


async def main():
    await set_bot_commands(bot)
    dp.include_router(rout)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())

