from typing import BinaryIO

from aiogram import types, Bot
from aiogram import Router
from aiogram import F
from aiogram.filters import Command
from aiogram.types import File

from src.bot.bot import BotSingleton
from src.core.domain.document_service import DocumentService
from src.core.domain.chat import ask

from datetime import date
from src.config import SettingsSingleton

router = Router()
settings = SettingsSingleton.get_instance()

@router.message(F.text, Command('start'))
async def start(message: types.Message):
    print(f'[BOT]: <{message.chat.id}> - /start')
    await message.answer("Привет! Отправь мне документ для загрузки или задай вопрос.")


@router.message(F.text, Command('chunks'))
async def get_chunks(message: types.Message):
    print(f'[BOT]: <{message.chat.id}> - /chunks')
    document_service = DocumentService()
    chunks: list[str] = document_service.get_chunks()

    for chunk in chunks:
        await message.answer(chunk)

@router.message(F.text, Command('search'))
async def search_document(message: types.Message):
    _, _, query = message.text.partition(' ')
    print(f'[BOT]: <{message.chat.id}> - /search {query}')
    document_service = DocumentService()
    context: str = document_service.search_with_formatting(query)

    await message.answer(context)

@router.message(F.text)
async def question(message: types.Message):
    thread_id: int = message.chat.id
    print(f'[BOT]: <{thread_id}> - {message.text}')
    answer = ask(message.text, str(thread_id))

    await message.answer(str(answer))


@router.message(F.document)
async def upload_document(message: types.Message):
    print(f'[BOT]: <{message.chat.id}> - file loaded')
    bot: Bot = BotSingleton.get_instance()
    doc_file: File = await bot.get_file(message.document.file_id)
    doc_file_bytes: BinaryIO | None = await bot.download_file(doc_file.file_path)
    if doc_file_bytes is None:
        await message.answer('Ошибка скачивания документа!')
        return
    
    content: str = doc_file_bytes.read().decode('utf-8')

    file_path = f'/app/fixtures/{message.document.file_name}-{message.from_user.id}.txt'
    with open(file_path, 'w', encoding='utf-8') as doc_file_write:
        doc_file_write.write(content)
    # Future:
    #document_service = DocumentService()
    #document_service.upload_from_text(content)
    #if message.caption is not None and message.caption.strip() != "":
    #    await message.answer('Документ загружен! Бот уже генерирует ответ на ваш вопрос')
    #    thread_id: int = message.chat.id
    #    print(f'[BOT]: <{thread_id}> - {message.caption}')
    #    answer = ask(message.caption, str(thread_id))
    #    await message.answer(str(answer))
    #else:
    #    await message.answer('Документ загружен!')
    await message.answer('Документ загружен!')