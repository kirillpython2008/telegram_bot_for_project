from asyncio import run
from os import getenv

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

from headers.user_routers import user_router
from headers.admin_routers import admin_router

load_dotenv()

TOKEN = getenv("BOT_TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot)

dp.include_router(router=user_router)
dp.include_router(router=admin_router)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    run(main())
