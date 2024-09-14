from aiogram.filters import Command
from aiogram import Router
from aiogram.types import Message

rout = Router()


@rout.message(Command("start"))
async def hendler_command_start(message: Message):
    await message.answer("hi")


@rout.message(Command("AddProduct"))
async def hendler_command_AddProduct(message: Message):
    user = message.text
