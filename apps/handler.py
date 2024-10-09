from aiogram.filters import Command
from aiogram import Router
from aiogram.types import Message
from config import download_path
from aiogram.types import FSInputFile
from converter import convert_time_string_to_seconds as conv
from YouTobeVideo import download_video_youtube
import asyncio
import os
from apps.TikTokVideo import download_tiktok_video

rout = Router()
process_lock = asyncio.Lock()
commands_list = [
    "/User_id - Получить свой ID пользователя",
    "/information - Дает информацию"
]

@rout.message(Command("start"))
async def handler_command_start(message: Message):
    commands_text = "\n".join(commands_list)
    await message.answer(f"Привет! Вот список доступных команд:\n{commands_text}")


@rout.message(Command("user_id"))
async def handler_id_user(message: Message):
    await message.answer(str(message.from_user.id))

@rout.message(Command("information"))
async def handler_command_start(message: Message):
    await message.answer(f"Ну короче, кидай ссылку, а я тебе перешлю видео.\nЕсли нужно скачать видео целиком: Скидываешь URL. \nЕсли нужно скачать 10 секунд, то указываете первый таймкод. \nЕсли нужен клип, то указываете два таймкода")

@rout.message(Command("Sponsor"))
async def handler_command_start(message: Message):
    await message.answer(f"Поддержать проект можно по этой ссылке:https://youtu.be/sYbo-BIOHmI?si=s1xH6_TlfllvuFHp")

@rout.message()
async def handler_command_add_product(message: Message):
    async with process_lock:
        clear_directory(download_path)
        global message_lowed
        try:
            text = message.text.split(' ')
            text = [item for item in text if item]
            length = len(text)
            start = conv(None if length < 2 else text[1])
            end = conv(None if length < 3 else text[2])
            url = text[0]

            if "youtube.com" in url or "youtu.be" in url:
                message_lowed = await message.answer("Загрузка...")
                if start is None:

                    download_video_youtube(url)
                else:
                    download_video_youtube(url, start, end)

                files = os.listdir(download_path)
                if files:
                    latest_file = files[0]
                    video_file_path = os.path.join(download_path, latest_file)
                    video = FSInputFile(video_file_path)
                    await message.answer_video(video)
                else:
                    await message.answer("Video was not found")

                await message_lowed.delete()
                await message.delete()


            elif "tiktok.com" in url or "vt.tiktok.com" in url:
                message_lowed = await message.answer("Загрузка...")
                download_tiktok_video(url)
                files = os.listdir(download_path)
                if files:
                    latest_file = files[0]
                    video_file_path = os.path.join(download_path, latest_file)
                    video = FSInputFile(video_file_path)
                    await message.answer_video(video)
                else:
                    await message.answer("Video was not found")

                await message_lowed.delete()
                await message.delete()
        finally:
            if message_lowed:
                await message_lowed.delete()
            await message.answer("Ошибка загрузки видео.")




def clear_directory(directory_path):
    """Удаляет все файлы из указанной папки."""
    try:
        files = os.listdir(directory_path)
        for file in files:
            file_path = os.path.join(directory_path, file)
            if os.path.isfile(file_path):
                os.remove(file_path)
        print(f"Все файлы из папки {directory_path} успешно удалены.")
    except Exception as e:
        print(f"Ошибка при удалении файлов из папки {directory_path}: {e}")