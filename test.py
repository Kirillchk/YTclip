import requests
from y2mate_api import first_query, second_query, third_query, Handler
from os import path, makedirs

# Прокси-сервер
#proxies = {
#    "http": "http://108.61.166.152:8080",
#    "https": "http://108.61.166.152:8080"
#}
#
## Создаём сессию requests с прокси
#session = requests.Session()
#session.proxies.update(proxies)

# Настройка обработчика
handler = Handler("")

# Переопределяем запросы для использования глобальной сессии requests с прокси
def download_video(video_url: str, output_dir: str):
    """Download video from YouTube and save to file"""
    try:
        # Настройка с глобальной сессией requests с прокси
        fq = first_query(video_url).main()
        sq = second_query(fq).main()
        third_dict = third_query(sq).main(format="mp4", quality="720p")

        # Создаем директорию для сохранения, если её нет
        if not path.exists(output_dir):
            makedirs(output_dir)

        # Проверяем размер видео и сохраняем его
        if third_dict.get("size"):
            size = third_dict["size"].split(" ")[0]
            if size[0].isdigit() and float(size) <= 200:  # Примерный лимит размера файла
                saved_to = handler.save(
                    third_dict, output_dir, progress_bar=False, disable_history=True
                )
                print(f"Video downloaded and saved to {saved_to}")
                return saved_to
            else:
                print("Video exceeds the file size limit.")
                return None
        else:
            print("Failed to get video size.")
            return None

    except Exception as e:
        print(f"Error occurred - {e}")
        return None


# Пример использования
video_url = "https://www.youtube.com/watch?v=7N3iGPsMAjQ"  # URL видео для скачивания
output_dir = "downloads"  # Директория для сохранения видео
downloaded_file = download_video(video_url, output_dir)
if downloaded_file:
    print(f"Video file available at: {downloaded_file}")
