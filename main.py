import requests
from bs4 import BeautifulSoup

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message, FSInputFile
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton, InlineKeyboardMarkup, \
    InlineKeyboardButton
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import ReplyKeyboardBuilder

import time
import asyncio
import sqlite3
from random import sample, choice


class Choose_country_season(StatesGroup):
    choose_count_state = State()
    choose_season_year = State()


class Price_footbollers(StatesGroup):
    country = State()


class Table_country(StatesGroup):
    contry = State()


class Game1(StatesGroup):
    expansive_player = State()
    raund = State()


class Game2(StatesGroup):
    raund = State()
    end = State()


# -------------------------------------------------------------------------------------------------------------------------------------------------
def scrapping_func():
    HEADERS = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'ru,en;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        # 'Cookie': 'cuid=URNWAmXzEi6m1RfvLywLAgB=; adtech_uid=5d6a8de7-e0cd-4a1e-a813-6ba3ff600e78%3Achampionat.com; _ym_uid=1710428723676643843; _ym_d=1710428723; _ga=GA1.2.207942962.1710428723; tmr_lvid=ba8f023a022541bf596badb14f13718e; tmr_lvidTS=1710428722927; top100_id=t1.648840.1046938194.1710428723132; chash=JHjcE50dnz; t3_sid_4422985=s1.1555167467.1710428723373.1710428868770.1.18; _gid=GA1.2.374741811.1712592006; domain_sid=ML0KHQslAcc8aOP3EjOxO%3A1712592006502; _ym_isad=2; _ym_visorc=b; vpuid=1712592009.248-3393906145093524; detect_count=0; topnews_tab=main; t3_sid_7643964=s1.984736811.1712592009244.1712592327444.1.22; t3_sid_7356279=s1.272884874.1712592009262.1712592327444.1.22; pushPageCount=18; last_visit=1712582126412%3A%3A1712592926412; _ga_YN3KE9VF4L=GS1.2.1712592006.2.1.1712592926.0.0.0; tmr_detect=0%7C1712592928956; t3_sid_648840=s1.1936531590.1712592005962.1712592988160.2.97; t3_sid_7726560=s1.1105528775.1712592005965.1712592988161.2.113',
        'Referer': 'https://www.championat.com/news/football/1.html',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 YaBrowser/24.1.0.0 Safari/537.36',
        'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "YaBrowser";v="24.1", "Yowser";v="2.5"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    url = 'https://www.championat.com/news/football/1.html'
    response = requests.get(url=url, headers=HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')

    block = soup.find_all('li', class_='news-item')

    spis = []
    for item in block:
        spis.append([item.find('div', class_='news-item__content').text.replace('\n', ''),
                     'https://www.championat.com' + item.find('a', class_='news-item__title').get('href')])

    return spis


async def send_photo(data):
    photo = FSInputFile(f'Трансферы {data[1].split()[0]}/{data[2]}.png')
    await bot.send_photo(chat_id=data[0], photo=photo)


def random_footbollers(spis, num):
    return sample(spis, k=num)


# -------------------------------------------------------------------------------------------------------------------------------------------------


bot = Bot(token='6910912601:AAGuk-ug_YZZ412jjMoW1RXHbftapThUrHY')
dp = Dispatcher()

murkub = ReplyKeyboardMarkup(
    keyboard=([KeyboardButton(text='📝 Последние новости 📝'), KeyboardButton(text='🎭 Трансферы 🎭')],
              [KeyboardButton(text='💰 Стоимости футболистов 💰'), KeyboardButton(text='📌Таблицы турниров📌')],
              [KeyboardButton(text='🕹 Мини-игры 🕹')]), resize_keyboard=True)


# ---
@dp.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        f'👋 Здравствуте, {message.from_user.last_name}!\nЯ помогу вам узнать много интересного о ФУТБОЛЕ ⚽\n😇 Пожалуйста, выберите интересующую категорию:',
        reply_markup=murkub)


@dp.message(F.text == '➡ НАЗАД ➡')
async def news(message: Message, state: FSMContext):
    news = scrapping_func()
    await message.answer('🧐 Выбирайте что вас еще интересует... 🧐', reply_markup=murkub)
    await state.clear()


# ---

@dp.message(F.text == '📝 Последние новости 📝')
async def news(message: Message):
    news = scrapping_func()
    await message.answer(f'На данный момент получено новостей в количестве: {len(news)} шт...',
                         reply_markup=ReplyKeyboardRemove())
    time.sleep(1)

    for i, elem in enumerate(news):
        await message.answer(f'👉 {i + 1}) {elem[0]}\n\n', reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text='Подробнее', url=elem[1])]]))
    await message.answer('Нажмите "➡ НАЗАД ➡, чтобы вернуться в меню"',
                         reply_markup=ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='➡ НАЗАД ➡')]],
                                                          resize_keyboard=True))


# ---

@dp.message(F.text == '🎭 Трансферы 🎭')
async def choose_country(message: Message, state: FSMContext):
    await state.set_state(Choose_country_season.choose_count_state)
    await message.answer('Выберите страну...', reply_markup=ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text='Англия 🇬🇧'), KeyboardButton(text='Германия 🇩🇪')],
        [KeyboardButton(text='Испания 🇪🇸'), KeyboardButton(text='Франция 🇫🇷')],
        [KeyboardButton(text='Италия 🇮🇹'), KeyboardButton(text='Россия 🇷🇺')]
    ], resize_keyboard=True))


@dp.message(F.text == 'Англия 🇬🇧')
async def _(message: Message, state: FSMContext):
    await state.update_data(choose_country=message.text)
    await message.answer('Выберите сезон и год...', reply_markup=ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text='Зима 2021'), KeyboardButton(text='Лето 2021')],
        [KeyboardButton(text='Зима 2022'), KeyboardButton(text='Лето 2022')],
        [KeyboardButton(text='Зима 2023'), KeyboardButton(text='Лето 2023')],
        [KeyboardButton(text='Зима 2024')]
    ], resize_keyboard=True))


@dp.message(F.text == 'Германия 🇩🇪')
async def _(message: Message, state: FSMContext):
    await state.update_data(choose_country=message.text)
    await message.answer('Выберите сезон и год...', reply_markup=ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text='Зима 2021'), KeyboardButton(text='Лето 2021')],
        [KeyboardButton(text='Зима 2022'), KeyboardButton(text='Лето 2022')],
        [KeyboardButton(text='Зима 2023'), KeyboardButton(text='Лето 2023')],
        [KeyboardButton(text='Зима 2024')]
    ], resize_keyboard=True))


@dp.message(F.text == 'Испания 🇪🇸')
async def _(message: Message, state: FSMContext):
    await state.update_data(choose_country=message.text)
    await message.answer('Выберите сезон и год...', reply_markup=ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text='Зима 2021'), KeyboardButton(text='Лето 2021')],
        [KeyboardButton(text='Зима 2022'), KeyboardButton(text='Лето 2022')],
        [KeyboardButton(text='Зима 2023'), KeyboardButton(text='Лето 2023')],
        [KeyboardButton(text='Зима 2024')]
    ], resize_keyboard=True))


@dp.message(F.text == 'Франция 🇫🇷')
async def _(message: Message, state: FSMContext):
    await state.update_data(choose_country=message.text)
    await message.answer('Выберите сезон и год...', reply_markup=ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text='Зима 2021'), KeyboardButton(text='Лето 2021')],
        [KeyboardButton(text='Зима 2022'), KeyboardButton(text='Лето 2022')],
        [KeyboardButton(text='Зима 2023'), KeyboardButton(text='Лето 2023')],
        [KeyboardButton(text='Зима 2024')]
    ], resize_keyboard=True))


@dp.message(F.text == 'Италия 🇮🇹')
async def _(message: Message, state: FSMContext):
    await state.update_data(choose_country=message.text)
    await message.answer('Выберите сезон и год...', reply_markup=ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text='Зима 2021'), KeyboardButton(text='Лето 2021')],
        [KeyboardButton(text='Зима 2022'), KeyboardButton(text='Лето 2022')],
        [KeyboardButton(text='Зима 2023'), KeyboardButton(text='Лето 2023')],
        [KeyboardButton(text='Зима 2024')]
    ], resize_keyboard=True))


@dp.message(F.text == 'Россия 🇷🇺')
async def _(message: Message, state: FSMContext):
    await state.update_data(choose_country=message.text)
    await message.answer('Выберите сезон и год...', reply_markup=ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text='Зима 2021'), KeyboardButton(text='Лето 2021')],
        [KeyboardButton(text='Зима 2022'), KeyboardButton(text='Лето 2022')],
        [KeyboardButton(text='Зима 2023'), KeyboardButton(text='Лето 2023')],
        [KeyboardButton(text='Зима 2024')]
    ], resize_keyboard=True))

    await state.set_state(Choose_country_season.choose_season_year)


# ---

@dp.message(F.text == 'Зима 2021')
async def _(message: Message, state: FSMContext):
    data = [message.chat.id]
    get_data_state = await state.get_data()

    data.append(get_data_state['choose_country'][:])

    await state.update_data(choose_season_year=message.text)

    get_data_state = await state.get_data()
    data.append(get_data_state['choose_season_year'])
    await send_photo(data)
    await state.clear()
    await message.answer('Нажмите "➡ НАЗАД ➡, чтобы вернуться в меню"',
                         reply_markup=ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='➡ НАЗАД ➡')]],
                                                          resize_keyboard=True))


@dp.message(F.text == 'Лето 2021')
async def _(message: Message, state: FSMContext):
    data = [message.chat.id]
    get_data_state = await state.get_data()

    data.append(get_data_state['choose_country'][:])

    await state.update_data(choose_season_year=message.text)

    get_data_state = await state.get_data()
    data.append(get_data_state['choose_season_year'])

    await send_photo(data)
    await state.clear()
    await message.answer('Нажмите "➡ НАЗАД ➡, чтобы вернуться в меню"',
                         reply_markup=ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='➡ НАЗАД ➡')]],
                                                          resize_keyboard=True))


@dp.message(F.text == 'Зима 2022')
async def _(message: Message, state: FSMContext):
    data = [message.chat.id]
    get_data_state = await state.get_data()

    data.append(get_data_state['choose_country'][:])

    await state.update_data(choose_season_year=message.text)

    get_data_state = await state.get_data()
    data.append(get_data_state['choose_season_year'])

    await send_photo(data)
    await state.clear()
    await message.answer('Нажмите "➡ НАЗАД ➡, чтобы вернуться в меню"',
                         reply_markup=ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='➡ НАЗАД ➡')]],
                                                          resize_keyboard=True))


@dp.message(F.text == 'Лето 2022')
async def _(message: Message, state: FSMContext):
    data = [message.chat.id]
    get_data_state = await state.get_data()

    data.append(get_data_state['choose_country'][:])

    await state.update_data(choose_season_year=message.text)

    get_data_state = await state.get_data()
    data.append(get_data_state['choose_season_year'])

    await send_photo(data)
    await state.clear()
    await message.answer('Нажмите "➡ НАЗАД ➡, чтобы вернуться в меню"',
                         reply_markup=ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='➡ НАЗАД ➡')]],
                                                          resize_keyboard=True))


@dp.message(F.text == 'Зима 2023')
async def _(message: Message, state: FSMContext):
    data = [message.chat.id]
    get_data_state = await state.get_data()

    data.append(get_data_state['choose_country'][:])

    await state.update_data(choose_season_year=message.text)

    get_data_state = await state.get_data()
    data.append(get_data_state['choose_season_year'])

    await send_photo(data)
    await state.clear()
    await message.answer('Нажмите "➡ НАЗАД ➡, чтобы вернуться в меню"',
                         reply_markup=ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='➡ НАЗАД ➡')]],
                                                          resize_keyboard=True))


@dp.message(F.text == 'Лето 2023')
async def _(message: Message, state: FSMContext):
    data = [message.chat.id]
    get_data_state = await state.get_data()

    data.append(get_data_state['choose_country'][:])

    await state.update_data(choose_season_year=message.text)

    get_data_state = await state.get_data()
    data.append(get_data_state['choose_season_year'])
    await send_photo(data)
    await state.clear()
    await message.answer('Нажмите "➡ НАЗАД ➡, чтобы вернуться в меню"',
                         reply_markup=ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='➡ НАЗАД ➡')]],
                                                          resize_keyboard=True))


@dp.message(F.text == 'Зима 2024')
async def _(message: Message, state: FSMContext):
    data = [message.chat.id]
    get_data_state = await state.get_data()
    print(get_data_state)
    data.append(get_data_state['choose_country'][:])

    await state.update_data(choose_season_year=message.text)
    print(get_data_state)

    get_data_state = await state.get_data()
    data.append(get_data_state['choose_season_year'])
    print(get_data_state)
    print(data)
    await send_photo(data)
    await state.clear()
    await message.answer('Нажмите "➡ НАЗАД ➡, чтобы вернуться в меню"',
                         reply_markup=ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='➡ НАЗАД ➡')]],
                                                          resize_keyboard=True))


# ---

@dp.message(F.text == '💰 Стоимости футболистов 💰')
async def prices(message: Message, state: FSMContext):
    await state.set_state(Price_footbollers.country)
    await message.answer('Выберите страну...', reply_markup=ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text='🇬🇧 Англия'), KeyboardButton(text='🇩🇪 Германия')],
        [KeyboardButton(text='🇪🇸 Испания'), KeyboardButton(text='🇫🇷 Франция')],
        [KeyboardButton(text='🇮🇹 Италия'), KeyboardButton(text='🇷🇺 Россия')]
    ], resize_keyboard=True))


@dp.message(F.text == '🇬🇧 Англия')
async def __(message: Message, state: FSMContext):
    await message.answer('Топ 50 самых дорогих футболстов Англии 🤑', reply_markup=ReplyKeyboardRemove())
    db = sqlite3.connect('basedata.db')
    cur = db.cursor()
    cur.execute('SELECT * FROM Англия')
    s = ''
    for item in cur.fetchall()[:51]:
        s += f'{item[0]}   --->   {item[1]}\n'
    await message.answer(s)
    await message.answer('Нажмите "➡ НАЗАД ➡, чтобы вернуться в меню"',
                         reply_markup=ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='➡ НАЗАД ➡')]],
                                                          resize_keyboard=True))
    await state.clear()


@dp.message(F.text == '🇩🇪 Германия')
async def __(message: Message, state: FSMContext):
    await message.answer('Топ 50 самых дорогих футболстов Германии 🤑', reply_markup=ReplyKeyboardRemove())
    db = sqlite3.connect('basedata.db')
    cur = db.cursor()
    cur.execute('SELECT * FROM Германия')
    s = ''
    for item in cur.fetchall()[:51]:
        s += f'{item[0]}   --->   {item[1]}\n'

    await message.answer(s)
    await message.answer('Нажмите "➡ НАЗАД ➡, чтобы вернуться в меню"',
                         reply_markup=ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='➡ НАЗАД ➡')]],
                                                          resize_keyboard=True))
    await state.clear()


@dp.message(F.text == '🇪🇸 Испания')
async def __(message: Message, state: FSMContext):
    await message.answer('Топ 50 самых дорогих футболстов Испании 🤑', reply_markup=ReplyKeyboardRemove())
    db = sqlite3.connect('basedata.db')
    cur = db.cursor()
    cur.execute('SELECT * FROM Испания')
    s = ''
    for item in cur.fetchall()[:51]:
        s += f'{item[0]}   --->   {item[1]}\n'

    await message.answer(s)
    await message.answer('Нажмите "➡ НАЗАД ➡, чтобы вернуться в меню"',
                         reply_markup=ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='➡ НАЗАД ➡')]],
                                                          resize_keyboard=True))
    await state.clear()


@dp.message(F.text == '🇫🇷 Франция')
async def __(message: Message, state: FSMContext):
    await message.answer('Топ 50 самых дорогих футболстов Франции 🤑', reply_markup=ReplyKeyboardRemove())
    db = sqlite3.connect('basedata.db')
    cur = db.cursor()
    cur.execute('SELECT * FROM Франция')
    s = ''
    for item in cur.fetchall()[:51]:
        s += f'{item[0]}   --->   {item[1]}\n'
    await message.answer(s)
    await message.answer('Нажмите "➡ НАЗАД ➡, чтобы вернуться в меню"',
                         reply_markup=ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='➡ НАЗАД ➡')]],
                                                          resize_keyboard=True))
    await state.clear()


@dp.message(F.text == '🇮🇹 Италия')
async def __(message: Message, state: FSMContext):
    await message.answer('Топ 50 самых дорогих футболстов Италии 🤑', reply_markup=ReplyKeyboardRemove())
    db = sqlite3.connect('basedata.db')
    cur = db.cursor()
    cur.execute('SELECT * FROM Италия')
    s = ''
    for item in cur.fetchall()[:51]:
        s += f'{item[0]}   --->   {item[1]}\n'

    await message.answer(s)
    await message.answer('Нажмите "➡ НАЗАД ➡, чтобы вернуться в меню"',
                         reply_markup=ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='➡ НАЗАД ➡')]],
                                                          resize_keyboard=True))
    await state.clear()


@dp.message(F.text == '🇷🇺 Россия')
async def __(message: Message, state: FSMContext):
    await message.answer('Топ 50 самых дорогих футболстов России 🤑', reply_markup=ReplyKeyboardRemove())
    db = sqlite3.connect('basedata.db')
    cur = db.cursor()
    cur.execute('SELECT * FROM Россия')
    s = ''
    for item in cur.fetchall()[:51]:
        s += f'{item[0]}   --->   {item[1]}\n'

    await message.answer(s)
    await message.answer('Нажмите "➡ НАЗАД ➡, чтобы вернуться в меню"',
                         reply_markup=ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='➡ НАЗАД ➡')]],
                                                          resize_keyboard=True))
    await state.clear()


@dp.message(F.text == '📌Таблицы турниров📌')
async def tables(message: Message, state: FSMContext):
    await state.set_state(Table_country.contry)
    await message.answer('Выберите страну...', reply_markup=ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text='🇬🇧 Англия 🇬🇧'), KeyboardButton(text='🇩🇪 Германия 🇩🇪')],
        [KeyboardButton(text='🇪🇸 Испания 🇪🇸'), KeyboardButton(text='🇫🇷 Франция 🇫🇷')],
        [KeyboardButton(text='🇮🇹 Италия 🇮🇹'), KeyboardButton(text='🇷🇺 Россия 🇷🇺')]
    ], resize_keyboard=True))


@dp.message(F.text == '🇬🇧 Англия 🇬🇧')
async def tables(message: Message, state: FSMContext):
    photo = FSInputFile(f'Фотки турниров/Англия.png')
    await bot.send_photo(chat_id=message.chat.id, photo=photo)
    await message.answer('Нажмите "➡ НАЗАД ➡, чтобы вернуться в меню"',
                         reply_markup=ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='➡ НАЗАД ➡')]],
                                                          resize_keyboard=True))
    await state.clear()


@dp.message(F.text == '🇩🇪 Германия 🇩🇪')
async def tables(message: Message, state: FSMContext):
    photo = FSInputFile(f'Фотки турниров/Германия.png')
    await bot.send_photo(chat_id=message.chat.id, photo=photo)
    await message.answer('Нажмите "➡ НАЗАД ➡, чтобы вернуться в меню"',
                         reply_markup=ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='➡ НАЗАД ➡')]],
                                                          resize_keyboard=True))
    await state.clear()


@dp.message(F.text == '🇪🇸 Испания 🇪🇸')
async def tables(message: Message, state: FSMContext):
    photo = FSInputFile(f'Фотки турниров/Испания.png')
    await bot.send_photo(chat_id=message.chat.id, photo=photo)
    await message.answer('Нажмите "➡ НАЗАД ➡, чтобы вернуться в меню"',
                         reply_markup=ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='➡ НАЗАД ➡')]],
                                                          resize_keyboard=True))
    await state.clear()


@dp.message(F.text == '🇫🇷 Франция 🇫🇷')
async def tables(message: Message, state: FSMContext):
    photo = FSInputFile(f'Фотки турниров/Франция.png')
    await bot.send_photo(chat_id=message.chat.id, photo=photo)
    await message.answer('Нажмите "➡ НАЗАД ➡, чтобы вернуться в меню"',
                         reply_markup=ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='➡ НАЗАД ➡')]],
                                                          resize_keyboard=True))
    await state.clear()


@dp.message(F.text == '🇮🇹 Италия 🇮🇹')
async def tables(message: Message, state: FSMContext):
    photo = FSInputFile(f'Фотки турниров/Италия.png')
    await bot.send_photo(chat_id=message.chat.id, photo=photo)
    await message.answer('Нажмите "➡ НАЗАД ➡, чтобы вернуться в меню"',
                         reply_markup=ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='➡ НАЗАД ➡')]],
                                                          resize_keyboard=True))
    await state.clear()


@dp.message(F.text == '🇷🇺 Россия 🇷🇺')
async def tables(message: Message, state: FSMContext):
    photo = FSInputFile(f'Фотки турниров/Россия.png')
    await bot.send_photo(chat_id=message.chat.id, photo=photo)
    await message.answer('Нажмите "➡ НАЗАД ➡, чтобы вернуться в меню"',
                         reply_markup=ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='➡ НАЗАД ➡')]],
                                                          resize_keyboard=True))
    await state.clear()


@dp.message(F.text == '🕹 Мини-игры 🕹')
async def games(message: Message):
    await message.answer('🎮 Выберите одну игру из представленный на клавиатуре...', reply_markup=ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text='👤 WHATS MY VALUE? 👤'), KeyboardButton(text='⚽ DRAFT ⚽')]],
        resize_keyboard=True))


sqore = 0


@dp.message(F.text == '👤 WHATS MY VALUE? 👤')
async def game1(message: Message, state: FSMContext):
    await message.answer(
        'Правила игры очень просты:\nВам будет предлагаться два футболиста.\nВаша задача угадать кто из них дороже, выбрав его на клавиатуре.\nИгра будет продолжаться до тех пор пока вы не ошибётесь.\nТак же вам будут начисляться очки за каждый пройденный раунд.\n\nНажмите ДАЛЕЕ для начала игры...',
        reply_markup=ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='✅ ДАЛЕЕ ✅')]], resize_keyboard=True))


@dp.message(F.text == '✅ ДАЛЕЕ ✅')
async def ready1(message: Message, state: FSMContext):
    bd = sqlite3.connect('basedata.db')
    cur = bd.cursor()

    spis = []
    for item in ['Англия', 'Германия', 'Россия', 'Испания', 'Франция', 'Италия']:
        cur.execute(f'SELECT * FROM {item}')
        spis += cur.fetchall()

    a, b = random_footbollers(spis, 2)
    name1, price1 = a[0], [a[1].split()[0].replace(',', '.'), a[1].split()[1]]
    name2, price2 = b[0], [b[1].split()[0].replace(',', '.'), b[1].split()[1]]

    await state.set_state(Game1.expansive_player)

    if price1[1] == price2[1] == 'млн':
        if float(price1[0]) > float(price2[0]):
            await state.update_data(expansive_player=name1)
        else:
            await state.update_data(expansive_player=name2)
    elif price1[1] == price2[1] == 'тыс':
        try:
            if int(price1[0]) > int(price2[0]):
                await state.update_data(expansive_player=name1)
            else:
                await state.update_data(expansive_player=name2)
        except:
            if float(price1[0]) > float(price2[0]):
                await state.update_data(expansive_player=name1)
            else:
                await state.update_data(expansive_player=name2)
    else:
        await state.update_data(expansive_player=name1)

    await state.set_state(Game1.raund)
    await message.answer(f'{a[0]}   ----   {b[0]}', reply_markup=ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=f'{name1}'), KeyboardButton(text=f'{name2}')]], resize_keyboard=True))


@dp.message(F.text == '🔄 Попробовать еще раз 🔄')
async def ddd(message: Message, state: FSMContext):
    global sqore
    sqore = 0

    await message.answer('Нажмите ДАЛЕЕ для начала игры...',
                         reply_markup=ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='✅ ДАЛЕЕ ✅')]],
                                                          resize_keyboard=True))


@dp.message(Game1.raund)
async def ddd(message: Message, state: FSMContext):
    data = await state.get_data()
    if message.text + ' ' == data['expansive_player']:
        global sqore
        sqore += 1
        await message.answer('Подтвердите свой выбор, нажав кнопку ДАЛЕЕ на клавиатуре',
                             reply_markup=ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='✅ ДАЛЕЕ ✅')]],
                                                              resize_keyboard=True))
    else:
        await message.answer(f'Увы, но допущена ошибка. ☠\nВашь счет: {sqore}\nМожете попробовать снова!',
                             reply_markup=ReplyKeyboardMarkup(keyboard=(
                                 [[KeyboardButton(text='🔄 Попробовать еще раз 🔄'), KeyboardButton(text='➡ НАЗАД ➡')]]),
                                 resize_keyboard=True))
        await state.clear()


# -----

list_player = []
list_bot = []
spis_all = []


@dp.message(F.text == '⚽ DRAFT ⚽')
async def game2(message: Message, state: FSMContext):
    await message.answer(
        'Правила очень просты:\nВам будет предложен список футболистов, из который вам предстоит выбрать самых дорогих.\nПротив вас будет играть бот, который тоже будет пытаться собрать команду как можно дороже.\nПобеждает тот кто соберет команду дороже чем у абонента.\n\nНажмите ❇ ПРОДОЛЖИТЬ ❇ для начала игры...',
        reply_markup=ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='❇ ПРОДОЛЖИТЬ ❇')]], resize_keyboard=True))
    bd = sqlite3.connect('basedata.db')
    cur = bd.cursor()

    spis = []
    for item in ['Англия', 'Германия', 'Россия', 'Испания', 'Франция', 'Италия']:
        cur.execute(f'SELECT * FROM {item}')
        spis += cur.fetchall()
    global spis_all

    spis_all = random_footbollers(spis, 22)


@dp.message(F.text == '❇ ПРОДОЛЖИТЬ ❇')
async def start_game2(message: Message, state: FSMContext):
    if spis_all:
        builder = ReplyKeyboardBuilder()
        for item in spis_all:
            builder.add(KeyboardButton(text=f'{item[0].strip()}'))
        builder.adjust(2)

        keyboard_murkab = builder.as_markup(resize_keyboard=True)

        await message.answer('Выберите футболиста...', reply_markup=keyboard_murkab)
        await state.set_state(Game2.raund)
    else:
        await message.answer('Игра окончена.Нажмите ✴ КОНЕЦ ИГРЫ ✴, чтобы узнать результат...\n',
                             reply_markup=ReplyKeyboardMarkup(keyboard=([[KeyboardButton(text='✴ КОНЕЦ ИГРЫ ✴')]]),
                                                              resize_keyboard=True))
        await state.set_state(Game2.end)


@dp.message(Game2.raund)
async def ddd(message: Message, state: FSMContext):
    global list_player, list_bot, spis_all

    player_choose = [item for item in spis_all if item[0].strip() == message.text][0]

    list_player.append(player_choose)
    spis_all.remove(player_choose)

    bot_choose = choice(spis_all)
    list_bot.append(bot_choose)
    spis_all.remove(bot_choose)

    await message.answer('Бот сделал свой выбор. Нажмите ПРОДОЛЖИТЬ...',
                         reply_markup=ReplyKeyboardMarkup(keyboard=([[KeyboardButton(text='❇ ПРОДОЛЖИТЬ ❇')]]),
                                                          resize_keyboard=True))


@dp.message(Game2.end)
async def ddd(message: Message, state: FSMContext):
    print(list_player)
    print(list_bot)

    sqore_player = 0
    for item in list_player:
        if item[1].split()[1] == 'млн':
            price = float(item[1].split()[0].replace(',', '.')) * 1000
        else:
            price = float(item[1].split()[0].replace(',', '.'))
        sqore_player += price

    sqore_bot = 0
    for item in list_bot:
        if item[1].split()[1] == 'млн':
            price = float(item[1].split()[0].replace(',', '.')) * 1000
        else:
            price = float(item[1].split()[0].replace(',', '.'))
        sqore_bot += price
    await message.answer('Идет подсчет стоимости...', reply_markup=ReplyKeyboardRemove())
    time.sleep(3)
    if sqore_player > sqore_bot:
        await message.answer(
            f'🏆 Вы выиграли! 🏆\nВы набрали команду дороже чем Бот.\nСтоимость вашей команды: {sqore_player / 1000} млн €.\nСтоимость команды бота: {sqore_bot / 1000} млн €.\n\nНажмите 🔄 ИГРАТЬ СНОВА 🔄,чтобы играть еще раз, или ➡ НАЗАД ➡, чтобы вернуться в меню...',
            reply_markup=ReplyKeyboardMarkup(
                keyboard=[[KeyboardButton(text='🔄 ИГРАТЬ СНОВА 🔄'), KeyboardButton(text='➡ НАЗАД ➡')]],
                resize_keyboard=True))
    elif sqore_player < sqore_bot:
        await message.answer(
            f'☠ Вы проиграли. ☠\nБот набрал команду дороже чем у вас.\nСтоимость вашей команды: {sqore_player / 1000} млн €.\nСтоимость команды бота: {sqore_bot / 1000} млн €.\n\nНажмите 🔄 ИГРАТЬ СНОВА 🔄,чтобы играть еще раз, или ➡ НАЗАД ➡, чтобы вернуться в меню...',
            reply_markup=ReplyKeyboardMarkup(
                keyboard=[[KeyboardButton(text='🔄 ИГРАТЬ СНОВА 🔄'), KeyboardButton(text='➡ НАЗАД ➡')]],
                resize_keyboard=True))
    else:
        await message.answer(
            f'🤭 Ого! Похоже вы набрали команду по стоимости такую же как и ваш соперник! 🤭\nСтоимость вашей команды: {sqore_player / 1000} млн €.\nСтоимость команды бота: {sqore_bot / 1000} млн €.\n\nНажмите 🔄 ИГРАТЬ СНОВА 🔄,чтобы играть еще раз, или ➡ НАЗАД ➡, чтобы вернуться в меню...',
            reply_markup=ReplyKeyboardMarkup(
                keyboard=[[KeyboardButton(text='🔄 ИГРАТЬ СНОВА 🔄'), KeyboardButton(text='➡ НАЗАД ➡')]],
                resize_keyboard=True))
    await state.clear()


@dp.message(F.text == '🔄 ИГРАТЬ СНОВА 🔄')
async def ___(message: Message, state: FSMContext):
    await message.answer('Нажмите ❇ ПРОДОЛЖИТЬ ❇ для начала игры...',
                         reply_markup=ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='❇ ПРОДОЛЖИТЬ ❇')]],
                                                          resize_keyboard=True))
    bd = sqlite3.connect('basedata.db')
    cur = bd.cursor()

    spis = []
    for item in ['Англия', 'Германия', 'Россия', 'Испания', 'Франция', 'Италия']:
        cur.execute(f'SELECT * FROM {item}')
        spis += cur.fetchall()
    global spis_all

    spis_all = random_footbollers(spis, 22)


# -------------------------------------------------------------------------------------------------------------------------------------------------

async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
