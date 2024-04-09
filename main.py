from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import asyncio

bot = Bot(token='6910912601:AAGuk-ug_YZZ412jjMoW1RXHbftapThUrHY')
dp = Dispatcher()

murkub = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text='📝 Последние новости 📝'), KeyboardButton(text='🎭 Трансферы 🎭')]],
    resize_keyboard=True)


@dp.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        f'👋 Здравствуте, {message.from_user.last_name}!\nЯ помогу вам узнать много интересного о ФУТБОЛЕ ⚽\n😇 Пожалуйста, выберите интересующую категорию:',
        reply_markup=murkub)


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())