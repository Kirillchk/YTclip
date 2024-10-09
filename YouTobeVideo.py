import time
import yt_dlp
from yt_dlp import download_range_func
from config import download_path
import browser_cookie3


cookies = getattr(browser_cookie3,'firefox')(domain_name='www.youtube.com')


def download_video_youtube(input_string, start_time=None, end_time=None):
    try:
        # Общие опции для yt-dlp
        yt_opts = {
            'verbose': True,
            'force_keyframes_at_cuts': True,
            'cookiesfrombrowser': ('firefox',),
            'cookies': cookies,
            'format': 'best[ext=mp4]',
            'outtmpl': f'{download_path}/%(title)s.%(ext)s',
        }

        # Добавление диапазона загрузки, если указаны start_time и end_time
        if start_time is not None:
            if end_time is not None:
                yt_opts['download_ranges'] = download_range_func(None, [(start_time, end_time)])
            else:
                yt_opts['download_ranges'] = download_range_func(None, [(start_time, start_time + 10)])

        # Download the video using yt-dlp with the specified options
        with yt_dlp.YoutubeDL(yt_opts) as ydl:
            ydl.download([input_string])
            return
    except:
        print()