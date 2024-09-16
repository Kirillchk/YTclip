import io
import yt_dlp as youtube_dl
import ffmpeg
from aiogram.filters import Command
from aiogram import Router, exceptions, types
from aiogram.types import Message
import requests


rout = Router()

YOUTUBE = "https://www.youtube.com/"


@rout.message(Command("start"))
async def hendler_command_start(message: Message):
    await message.answer("hi")

@rout.message(Command("user_id"))
async def hendler_user_id(message: Message):
    await message.answer(str(message.chat.id))

@rout.message()
async def handler_command_add_product(message: Message):
    if YOUTUBE in message.text:
        url = message.text