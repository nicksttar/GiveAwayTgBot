import asyncio

from aiogram import Bot, Dispatcher
from config import TOKEN_API
from bot_models import classic_model, random_mode
from menu import mainkb, useit, aboutkb, pagination


bot = Bot(TOKEN_API, parse_mode='HTML')
dp = Dispatcher()

# Main bot function
async def main():

    dp.include_routers(mainkb.router, useit.router, aboutkb.router,
                       pagination.router, classic_model.router, random_mode.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
