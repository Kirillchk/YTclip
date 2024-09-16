from aiogram.filters import Command
from aiogram import Router
from aiogram.types import Message
from config import adminMainListId

rout = Router()

adminUserListId = [

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


UrlYOUTOBE = "https://www.youtube.com/"

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

@rout.message()
async def hendler_command_AddProduct(message: Message):
    if UrlYOUTOBE in message.text and message.from_user.id in adminUserListId or message.from_user.id in adminMainListId:
        await message.answer("youtobe url")
