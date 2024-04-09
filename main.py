from aiogram import Bot, Dispatcher
import asyncio

bot = Bot(token='6910912601:AAGuk-ug_YZZ412jjMoW1RXHbftapThUrHY')
dp = Dispatcher()

async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())