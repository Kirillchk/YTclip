from config import download_path
import yt_dlp
import browser_cookie3

cookies = getattr(browser_cookie3,'firefox')(domain_name='www.tiktok.com')

def download_tiktok_video(input_string):
    # Configure yt-dlp options
#    yt_opts_list = {
#        'verbose': True,
#        'cookies': cookies,
#        'listformats': True,  # Параметр для вывода всех доступных форматов
#    }
    yt_opts = {
        'verbose': True,
        'force_keyframes_at_cuts': True,
        'cookies': cookies,
        'format': 'worst',
        'outtmpl': f'{download_path}/%(title)s.%(ext)s',
    }
    try:
        #with yt_dlp.YoutubeDL(yt_opts_list) as ydl:
        #    ydl.extract_info(input_string, download=False)  # Скачивание не производится
        with yt_dlp.YoutubeDL(yt_opts) as ydl:
            ydl.download(input_string)
    except Exception as e:
        print(f"Ошибка при загрузке видео: {e}")


