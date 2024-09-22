import os
import aiohttp
import asyncio
from pathlib import Path

# Ссылка на видео TikTok
link = "https://vt.tiktok.com/ZS2CBafX9/"
# Директория для сохранения видео
directory = "downloads"
# Прокси-сервер для обхода блокировки
proxy_url = "http://123.45.67.89:8080"  # Замените на свой прокси-сервер

# Создаем папку для загрузки файлов
Path(directory).mkdir(exist_ok=True)

async def download_video(url):
    video_filename = os.path.join(directory, "tiktok_video.mp4")

    # Используем aiohttp для скачивания видео с прокси
    async with aiohttp.ClientSession() as session:
        async with session.get(url, proxy=proxy_url) as response:
            if response.status == 200:
                # Сохраняем видео в файл
                with open(video_filename, 'wb') as f:
                    f.write(await response.read())
                print(f"Видео скачано и сохранено по пути: {video_filename}")
            else:
                print(f"Ошибка загрузки видео, статус: {response.status}")

async def main():
    # Начинаем скачивание видео
    print(f"Скачивание видео по ссылке: {link}")
    await download_video(link)

# Запуск асинхронного процесса
if __name__ == "__main__":
    asyncio.run(main())
