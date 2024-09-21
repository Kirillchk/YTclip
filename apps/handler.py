from aiogram.filters import Command
from aiogram import Router
from aiogram.types import Message
from config import adminMainListId, download_path
from config import adminMainListId, download_path, trimed_path, trimed_video_file_path
from YouTobeVideo import download_video_youtube
from aiogram.types import InputFile, FSInputFile
from Trim import trim_video
from converter import convert_time_string_to_tuple as conv
from aiogram import types
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


@rout.message()
async def handler_command_AddProduct(message: Message):
    url = message.text

    # Проверка, если это короткий URL
    if url.startswith(UrlYOUTOBE[1]):
        # Заменяем короткий URL на полный
        url = url.replace("https://youtu.be/", "https://www.youtube.com/watch?v=")

    if url.startswith(UrlYOUTOBE[0]) and (
            message.from_user.id in adminUserListId or message.from_user.id in adminMainListId):
        # Загружаем видео по ссылке
        download_video_youtube(UrlYOUTOBE[0])
        print(1)

        video_dir = download_path
        files = os.listdir(video_dir)
        if files:
            # Получаем самый новый файл по времени изменения
            print(2)
            latest_file = max(files, key=lambda f: os.path.getmtime(os.path.join(video_dir, f)))
            video_file_path = os.path.join(video_dir, latest_file)
            # Create FSInputFile object
            video = FSInputFile(video_file_path)
            await message.answer_video(video)

            # Удаляем файл после отправки
            time_data = message.text.split()
            print(time_data)
            # Pass the file path string to trim_video function
            trim_video(video_file_path, trimed_path, conv(time_data[1]), conv(time_data[2]))
            # latest_file = max(files, key=lambda f: os.path.getmtime(os.path.join(trimed_path, f)))
            # trimed_video_file_path = r"E:\code\Trimed vids\trimmed_video.mp4"
            trimed_video = FSInputFile(trimed_video_file_path)
            await message.answer_video(trimed_video)
            print(3)
            os.remove(video_file_path)
        else:
            await message.answer("Видео не найдено в папке.")