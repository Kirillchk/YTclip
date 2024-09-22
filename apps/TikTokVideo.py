<<<<<<< HEAD
import os
import aiohttp
import asyncio
from pathlib import Path
=======
import aiohttp
import asyncio
import os
from config import download_path  # Подключаем путь для сохранения видео


async def download_tiktok_video(url, save_path):
    """
    Скачивает видео по указанной ссылке и сохраняет его в указанной директории.
    """
    # Проверяем, что папка для загрузок существует
    os.makedirs(save_path, exist_ok=True)

    # Имя файла для сохранения
    file_name = os.path.join(save_path, 'tiktok_video.mp4')

    # Заголовки, имитирующие запрос от браузера
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers, allow_redirects=True) as response:
            if response.status == 200:
                # Записываем файл в локальную директорию
                with open(file_name, 'wb') as f:
                    while True:
                        chunk = await response.content.read(1024)  # Чтение по частям
                        if not chunk:
                            break
                        f.write(chunk)
                print(f"Видео успешно сохранено в {file_name}")
            else:
                print(f"Ошибка при скачивании видео. Статус: {response.status}")


# Пример использования

#url = "https://www.tiktok.com/@username/video/1234567890"  # Прямая ссылка на видео TikTok
url = "https://vt.tiktok.com/ZS2CBafX9/"
#url = "https://www.youtube.com/watch?v=unjjUqBQlVY"

# Запуск асинхронной задачи
>>>>>>> 4f6b80bfdd67d5d10af9fe14002b7c98657a1cfb

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
