import os
import time
import json
import requests
from dotenv import load_dotenv

from aiogram.client.default import DefaultBotProperties
from aiogram import Bot, Dispatcher  # бот, диспетчер
from aiogram import F  # магический фильтр
from aiogram.filters import Command, CommandStart  # фильтры
from aiogram.types import Message, ContentType  # апдейт Message, ContentType

from config import config
from pprint import pprint

load_dotenv()

API_URL = 'https://api.telegram.org/bot'
TOKEN = config['TEST_TOKEN']

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode='HTML'))


dp = Dispatcher()


# __________ HANDLERS __________
# TODO: Разнести функции по хэндлерам
# TODO: Добавить проверку на наличие такого скачиваемого файлы в save_dir


@dp.message(CommandStart())
async def process_command_start(message: Message):
    await message.answer(config['start_message'])


@dp.message(Command(commands=['help']))
async def process_command_help(message: Message):
    await message.answer(config['help_message'])


@dp.message(Command(commands=['contacts']))
async def process_command_contacts(message: Message):
    await message.answer(config['contacts'])


@dp.message(F.document)
async def document_loader(message: Message):
    doc = message.document
    file_name, file_id = doc.file_name, doc.file_id
    try:
        destination = os.path.join(config['save_dir'], file_name)
        await bot.download(file_id, destination)
    except Exception as error:
        print(f'Ошибка после получения документа: {error}')
        await message.answer(f"Файл '{file_name}' не получен.")
    else:
        await message.answer(f"Файл '{file_name}' успешно получен.")


# TODO: исправить
@dp.message(F.photo)
async def document_loader(message: Message):
    pprint(json.loads(message.json()))
    await message.answer('Получено фото')
    await message.answer("message_id:", message.message_id, "media_group_id", message.media_group_id)
    photo_id, photo_name = message.photo[-1].file_id, message.photo[-1].file_unique_id
    try:
        destination = os.path.join(config['save_dir'], photo_name, '.jpg')
        await bot.download(photo_id, destination)
    except Exception as error:
        print(f'Ошибка после получения документа: {error}')
        await message.answer(f"Фото '{photo_name}' не получено.")
    else:
        await message.answer(f"Фото '{photo_name}' успешно получено.")


@dp.message()
async def process_other_messages(message: Message):
    pprint(json.loads(message.json()))
    await message.answer(f"Неизвестная команда")


if __name__ == '__main__':
    dp.run_polling(bot, polling_timeout=7)
