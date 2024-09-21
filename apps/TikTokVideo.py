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

asyncio.run(download_tiktok_video(url, download_path))
