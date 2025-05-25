import asyncio
import logging
import sys
from os import getenv

from timetable import today, tomorrow

from aiogram import Bot, Dispatcher, types, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message

TOKEN = getenv("TOKEN")

users = []

dp = Dispatcher()


@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    user_id = message.from_user.id
    users.append(user_id)
    kb = [
        [
            types.KeyboardButton(text="Сегодня"),
            types.KeyboardButton(text="Завтра")
        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Выберите день"
    )
    await message.answer("На какой день показать расписание?", reply_markup=keyboard)


@dp.message(F.text.lower() == "сегодня")
async def lessons_today(message: types.Message):
    await message.answer(today)


@dp.message(F.text.lower() == "завтра")
async def lessons_tomorrow(message: types.Message):
    await message.answer(tomorrow)


@dp.message()
async def echo_handler(message: Message) -> None:
    await message.answer("Данного запроса нет, все возможные запросы имеются на кнопках")



async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())

