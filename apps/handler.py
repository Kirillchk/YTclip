from aiogram.filters import Command
from aiogram import Router
from aiogram.types import Message
from config import adminMainListId, download_path, trimed_path, trimed_video_file_path
from YouTobeVideo import download_video_youtube
from aiogram.types import InputFile, FSInputFile
from Trim import trim_video
from converter import convert_time_string_to_tuple as conv
from aiogram import types
import asyncio
import os

rout = Router()

adminUserListId = [

]

UrlYOUTOBE = [
    "https://www.youtube.com/",
    "https://youtu.be/"
]

# Список доступных команд
commands_list = [
    "/start - Начало работы с ботом",
    "/User_id - Получить свой ID пользователя",
    "/RemoveAdmin [id] - Удалить администратора (доступно только главному администратору)",
    "/AddAdmin [id] - Добавить администратора",
]

@rout.message(Command("start"))
async def handler_command_start(message: Message):
    commands_text = "\n".join(commands_list)
    await message.answer(f"Привет! Вот список доступных команд:\n{commands_text}")


@rout.message(Command("User_id"))
async def handler_id_user(message: Message):
    await message.answer(str(message.from_user.id))


@rout.message(Command("RemoveAdmin"))
async def handler_remove_admin(message: Message):
    if message.from_user.id in adminMainListId:  # Проверяем, что пользователь — главный администратор
        try:
            # Получаем ID администратора, которого нужно удалить
            remove_admin_id = int(message.text.split()[1])

            if remove_admin_id in adminUserListId:
                adminUserListId.remove(remove_admin_id)  # Удаляем администратора из списка
                await message.answer(f"Пользователь {remove_admin_id} удален из списка администраторов.")
            else:
                await message.answer(f"Пользователь {remove_admin_id} не является администратором.")
        except (IndexError, ValueError):
            await message.answer("Пожалуйста, укажите корректный ID пользователя. Пример: /RemoveAdmin 12345678")
    else:
        await message.answer("Бренный червь, у тебя нет права удалять админов. Склонись перед истинными админами.")



@rout.message(Command("AddAdmin"))
async def handler_add_admit(message: Message):
    if message.from_user.id in adminUserListId or message.from_user.id in adminMainListId:  # Проверка, что отправитель - администратор
        try:
            # Получаем аргумент команды (id нового администратора)
            new_admin_id = int(message.text.split()[1])  # Берем второй элемент сообщения (после /AddAdmin)

            if new_admin_id not in adminUserListId:
                adminUserListId.append(new_admin_id)  # Добавляем новый ID в список администраторов
                await message.answer(f"Пользователь {new_admin_id} добавлен в администраторы.")
            else:
                await message.answer("Этот пользователь уже является администратором.")
        except (IndexError, ValueError):
            await message.answer("Пожалуйста, укажите корректный ID пользователя. Пример: /AddAdmin 12345678")
    else:
        await message.answer("У вас нет прав для добавления администраторов.")


UrlYOUTOBE = [
    "https://www.youtube.com/",
    "https://youtu.be/"
]

# Очередь для обработки ссылок
link_queue = asyncio.Queue()
processing = False  # Флаг для отслеживания, выполняется ли обработка

import asyncio


# Функция для обработки очереди
async def process_queue():
    global processing
    while not link_queue.empty():  # Пока есть ссылки в очереди
        url, message = await link_queue.get()  # Извлекаем ссылку и сообщение
        processing = True  # Устанавливаем флаг, что началась обработка

        try:
            await process_link(url, message)  # Обрабатываем ссылку
        except Exception as e:
            await message.answer(f"Произошла ошибка при обработке видео: {str(e)}")

        link_queue.task_done()  # Помечаем задачу как выполненную
    processing = False  # Сбрасываем флаг после завершения обработки


# Основная функция обработки видео
async def process_link(url, message):
    # Отправляем сообщение о загрузке
    loading_message = await message.answer("Загрузка...")

    try:
        # Загружаем видео по ссылке в отдельном потоке
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, download_video_youtube, url.split()[0])
        print(1)

        video_dir = download_path
        files = os.listdir(video_dir)
        if files:
            print(2)
            latest_file = max(files, key=lambda f: os.path.getmtime(os.path.join(video_dir, f)))
            video_file_path = os.path.join(video_dir, latest_file)

            # Create FSInputFile object
            video = FSInputFile(video_file_path)
            time_data = message.text.split()

            # Проверка и обрезка видео
            if len(time_data) > 1:
                try:
                    trim_video(video_file_path, trimed_path, conv(time_data[1]), conv(time_data[2]))
                    trimed_video = FSInputFile(trimed_video_file_path)
                    await message.answer_video(trimed_video)
                    os.remove(video_file_path)
                    os.remove(trimed_video_file_path)
                except Exception as e:
                    await message.answer(f"Ошибка при обрезке видео: {str(e)}")
            else:
                await message.answer_video(video)

        else:
            await message.answer("Видео не найдено в папке.")

    except asyncio.TimeoutError:
        await message.answer("Скачивание видео заняло слишком много времени и было прервано.")
    except Exception as e:
        await message.answer(f"Произошла ошибка при обработке: {str(e)}")

    finally:
        # Удаляем сообщение пользователя независимо от успеха или ошибки
        try:
            await message.bot.delete_message(message.chat.id, message.message_id)
        except Exception as delete_error:
            await message.answer(f"Не удалось удалить сообщение пользователя: {str(delete_error)}")

        # Удаляем сообщение о загрузке после завершения
        try:
            await message.bot.delete_message(message.chat.id, loading_message.message_id)
        except Exception as loading_delete_error:
            await message.answer(f"Не удалось удалить сообщение о загрузке: {str(loading_delete_error)}")

        # Удаляем все файлы из папки
        delete_all_files_in_directory(download_path)



def delete_all_files_in_directory(directory_path):
    if not os.path.exists(directory_path):
        return f"Папка {directory_path} не существует."

    try:
        for filename in os.listdir(directory_path):
            file_path = os.path.join(directory_path, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)
        return f"Все файлы в папке {directory_path} удалены."
    except Exception as e:
        return f"Ошибка при удалении файлов: {str(e)}"


# Обработчик сообщений с ссылками
@rout.message()
async def handler_command_AddProduct(message: Message):
    global processing
    url = message.text

    # Проверка, если это короткий URL
    if url.startswith(UrlYOUTOBE[1]):
        # Заменяем короткий URL на полный
        url = url.replace("https://youtu.be/", "https://www.youtube.com/watch?v=")

    if url.startswith(UrlYOUTOBE[0]) and (
            message.from_user.id in adminUserListId or message.from_user.id in adminMainListId):
        # Добавляем ссылку и сообщение в очередь
        await link_queue.put((url, message))

        # Если нет активной обработки, запускаем обработку очереди
        if not processing:
            await process_queue()