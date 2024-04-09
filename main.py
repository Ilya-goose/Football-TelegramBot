from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import asyncio
import requests
from bs4 import BeautifulSoup

bot = Bot(token='6910912601:AAGuk-ug_YZZ412jjMoW1RXHbftapThUrHY')
dp = Dispatcher()

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