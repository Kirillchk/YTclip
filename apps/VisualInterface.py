from aiogram import Bot
from aiogram.types import BotCommand


async def set_bot_commands(bot: Bot):
    commands = [
        BotCommand(command="start", description="Запуск бота"),
        BotCommand(command="addadmin", description="Добавить администратора"),
        BotCommand(command="removeadmin", description="Удалить администратора")
    ]
    try:
        await bot.set_my_commands(commands)
    except Exception as e:
        print(f"Error setting bot commands: {e}")
