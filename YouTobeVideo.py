from config import download_path
import yt_dlp
from yt_dlp.utils import download_range_func


#class DownloadHandler(FileSystemEventHandler):
#    def __init__(self):
#        super().__init__()
#        self.download_completed = False
#
#    def on_created(self, event):
#        if event.src_path.endswith('.mp4'):
#            print(f"Download started: {event.src_path}")
#        elif event.src_path.endswith('.part'):
#            print(f"Download in progress: {event.src_path}")
#
#    def on_modified(self, event):
#        if event.src_path.endswith('.mp4'):
#            self.download_completed = True
#            print(f"Download completed: {event.src_path}")
#
#
#def watch_downloads(path, handler):
#    observer = Observer()
#    observer.schedule(handler, path, recursive=False)
#    observer.start()
#    return observer
#
#
#def wait_for_download(path, timeout=60):
#    end_time = time.time() + timeout
#    handler = DownloadHandler()
#    observer = watch_downloads(path, handler)
#    try:
#        while time.time() < end_time:
#            time.sleep(1)  # Allow time for events to be captured
#            # Check if the directory has non-temporary files (i.e., no '.part' extension)
#            downloaded_files = [f for f in os.listdir(path) if not f.endswith('.part')]
#            if downloaded_files:  # If there are any files, return True
#                return True
#            if handler.download_completed:  # Also return True if the download handler detects completion
#                return True
#    finally:
#        observer.stop()
#        observer.join()
#
#    print("Download did not complete in the given time.")
#    return False

start_time = 0

def download_video_youtube(input_string, start_time=None, end_time=None):
    # Общие опции для yt-dlp
    yt_opts = {
        'verbose': True,
        'force_keyframes_at_cuts': True,
        'cookiesfrombrowser': ('firefox',),
        'cookies': r'cookies-youtube-com.txt',
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

