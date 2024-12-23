import asyncio
import logging
import time
from sys import exec_prefix

from aiogram import Bot

import config
from handlers import dp

async def main():
    bot = Bot(token=config.BOT_TOKEN)
    while True:
        try:
            await dp.start_polling(bot)
        except Exception as e:
            print(f'Ошибка: {e}')
            time.sleep(5)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())