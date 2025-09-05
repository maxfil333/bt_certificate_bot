import os
import io
import re
from typing import Literal
from PyPDF2 import PdfReader
from datetime import datetime
from aiogram.types import Message

from src.logger import logger
from src.config import config


# __________ COMMON __________

def sanitize_filename(filename: str) -> str:
    try:
        # Заменяем все недопустимые символы на пробелы
        sanitized = re.sub(r'[\<\>\/\"\\\|\?\*]', ' ', filename)
        # Убираем повторяющиеся пробелы
        sanitized = re.sub(r'\s+', ' ', sanitized)
        # Убираем пробелы в начале и конце строки
        sanitized = sanitized.strip()
        return sanitized
    except Exception:
        return filename


def get_unique_filename(filepath):
    if not os.path.exists(filepath):
        return filepath
    else:
        base, ext = os.path.splitext(filepath)
        counter = 1
        while os.path.exists(f"{base}({counter}){ext}"):
            counter += 1
        return f"{base}({counter}){ext}"


def showlog_message_info(message: Message, message_type: Literal['file'] | Literal['authorization']):
    logger.print(datetime.now().strftime('%d.%m.%Y %H:%M:%S'))
    try:
        if message_type == 'file':
            text = f"""
            send file:
            {message.message_id}
            {message.from_user.id}, {message.from_user.first_name}, {message.from_user.last_name}, {message.from_user.username}
            {message.document.file_name}, {message.document.mime_type}
            """
        else:
            text = f"""
            authorization:
            {message.message_id}
            {message.from_user.id}, {message.from_user.first_name}, {message.from_user.last_name}, {message.from_user.username}
            """
        logger.print(text)
    except Exception as e:
        logger.print(f'error: {e}')
        logger.print(message.model_dump_json(indent=4, exclude_none=True))

    try:
        logger.save(config['log_folder'])
        logger.clear()
    except Exception as e:
        print('showlog_message_info error:', e)


def is_pdf_valid(pdf_data: str | bytes) -> bool:
    """
    Проверяет, открывается ли PDF.
    pdf_data: путь к файлу или байты
    """
    try:
        reader = PdfReader(pdf_data) if isinstance(pdf_data, str) else PdfReader(io.BytesIO(pdf_data))
        # Попробуем получить хотя бы одну страницу
        _ = reader.pages[0]
        return True
    except Exception:
        return False
