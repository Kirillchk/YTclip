#import requests
#from y2mate_api import first_query, second_query, third_query, Handler
#from os import path, makedirs
#
## Прокси-сервер
#proxies = {
#    "http": "http://108.61.166.152:8080",
#    "https": "http://108.61.166.152:8080"
#}
#
## Создаём сессию requests с прокси
#session = requests.Session()
#session.proxies.update(proxies)
#
## Настройка обработчика
#handler = Handler("")
#
## Переопределяем запросы для использования глобальной сессии requests с прокси
#def download_video(video_url: str, output_dir: str):
#    """Download video from YouTube and save to file"""
#    try:
#        # Настройка с глобальной сессией requests с прокси
#        fq = first_query(video_url).main()
#        sq = second_query(fq).main()
#        third_dict = third_query(sq).main(format="mp4", quality="720p")
#
#        # Создаем директорию для сохранения, если её нет
#        if not path.exists(output_dir):
#            makedirs(output_dir)
#
#        # Проверяем размер видео и сохраняем его
#        if third_dict.get("size"):
#            size = third_dict["size"].split(" ")[0]
#            if size[0].isdigit() and float(size) <= 200:  # Примерный лимит размера файла
#                saved_to = handler.save(
#                    third_dict, output_dir, progress_bar=False, disable_history=True
#                )
#                print(f"Video downloaded and saved to {saved_to}")
#                return saved_to
#            else:
#                print("Video exceeds the file size limit.")
#                return None
#        else:
#            print("Failed to get video size.")
#            return None
#
#    except Exception as e:
#        print(f"Error occurred - {e}")
#        return None
#
#
## Пример использования
#video_url = "https://www.youtube.com/watch?v=7N3iGPsMAjQ"  # URL видео для скачивания
#output_dir = "downloads"  # Директория для сохранения видео
#downloaded_file = download_video(video_url, output_dir)
#if downloaded_file:
#    print(f"Video file available at: {downloaded_file}")
#

from y2mate_api import Handler
import os
from tabulate import tabulate

# Функция очистки консоли для Windows и Linux/MacOS
def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

# Функция вывода приветственного баннера
def print_banner():
    print("=======================================")
    print("    Welcome to the YouTube Downloader   ")
    print("=======================================")

# Очищаем консоль и выводим баннер
clear_console()
print_banner()

# Получаем URL видео от пользователя
videoURL = str(input("Enter Video Link: "))

# Очищаем консоль и снова выводим баннер
clear_console()
print_banner()
print("Looking for Available Qualities...")

# Инициализируем API с указанным видео
api = Handler(videoURL)

# Указываем только 360p как целевое качество
target_quality = '360p'

urlList = []

# Функция для получения информации о видео
def getVidInfo(r):
    for video_metadata in api.run(quality=r):
        q = video_metadata.get("q")
        dlink = video_metadata.get("dlink")
        size = video_metadata.get("size")

        if dlink is None:
            pass
        else:
            urlList.append([q, size, dlink])

# Получаем информацию только для 360p
getVidInfo(target_quality)

# Если 360p доступно, продолжаем
if urlList:
    showList = {}
    for count, item in enumerate(urlList, 1):
        del item[2]  # Удаляем ссылку на загрузку из списка
        q = item[0]
        size = item[1]
        showList.update({count: {"q": q, "size": size}})

    # Отображаем список доступных видео (в нашем случае это только 360p)
    def showQTable():
        tableList = []
        for count, item in enumerate(showList, 1):
            q = showList[item]["q"]
            size = showList[item]["size"]
            tableList.append([count, q, size])
        print(tabulate(tableList, headers=["Q-No", "Quality", "Size"], tablefmt="heavy_grid"))

    showQTable()

    # Указываем, что мы загружаем видео в 360p автоматически
    clear_console()
    print_banner()
    print("Downloading 360p... Please wait!\n")

    mediaPath = f"{os.getcwd()}/vids"

    # Загружаем видео в указанную директорию
    for video_metadata in api.run(quality=showList[1]["q"]):  # Индекс всегда 1, так как только один вариант
        if not os.path.exists(mediaPath):
            os.makedirs(mediaPath)

        api.save(third_dict=video_metadata, dir="vids", progress_bar=True)

        vidFileName = f"{video_metadata['title']} {video_metadata['vid']}_{video_metadata['fquality']}.{video_metadata['ftype']}"
        print("Downloading:", vidFileName)

    # Очищаем экран и выводим сообщение о завершении загрузки
    clear_console()
    print_banner()
    print(f"Download Completed:\n{vidFileName} ✅")
    print(f"\nPlease Check the 'vids' Folder for your files!\n")

else:
    print("360p quality is not available for this video.")
