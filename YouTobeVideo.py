import pyautogui
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import download_path, gecko_driver_path, firefox_binary_path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

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

    # Wait until the 'loading_img' display property becomes 'none'
    WebDriverWait(driver, 10).until(
        lambda _: driver.find_element(By.ID, "loading_img").get_attribute("style").find("display: none") != -1
    )

    WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.LINK_TEXT, 'Download'))
    ).click()

    WebDriverWait(driver, 5).until(
        EC.number_of_windows_to_be(2)
    )
    time.sleep(1)
    driver.switch_to.window(driver.window_handles[-1])
    video_elements = driver.find_elements(By.TAG_NAME, 'video')
    if video_elements:
        print('Video element found, proceeding with download...')

        # Execute JavaScript to create a download link for the video and click it
        actions = ActionChains(driver)
        actions.context_click(video_elements[0]).perform()
        print('Context menu opened')

        # Simulate pressing down arrow to navigate to 'Save As' and press Enter
        time.sleep(1)

        for _ in range(5):
            pyautogui.press('up')
        pyautogui.press('enter')
        time.sleep(2)
        pyautogui.press('enter')

        print('Save As initiated')

        is_downloaded = wait_for_download(download_path)
        if is_downloaded:
            print("Downloaded successfully")
            driver.quit()
        else:
            print("Not downloaded")
    else:
        print("No video element found. Executing alternative logic...")
        # Alternative logic when no video is found
        is_downloaded = wait_for_download(download_path)
        if is_downloaded:
            print("Downloaded successfully")
            driver.quit()
        else:
            print("Not downloaded")


class DownloadHandler(FileSystemEventHandler):
    def __init__(self):
        super().__init__()
        self.download_completed = False

    def on_created(self, event):
        if event.src_path.endswith('.mp4'):
            print(f"Download started: {event.src_path}")
        elif event.src_path.endswith('.part'):
            print(f"Download in progress: {event.src_path}")

    def on_modified(self, event):
        if event.src_path.endswith('.mp4'):
            self.download_completed = True
            print(f"Download completed: {event.src_path}")


def watch_downloads(path, handler):
    observer = Observer()
    observer.schedule(handler, path, recursive=False)
    observer.start()
    return observer


def wait_for_download(path, timeout=60):
    end_time = time.time() + timeout
    handler = DownloadHandler()
    observer = watch_downloads(path, handler)

    try:
        while time.time() < end_time:
            time.sleep(1)  # Allow time for events to be captured
            if handler.download_completed:
                return True
    finally:
        observer.stop()
        observer.join()

    print("Download did not complete in the given time.")
    return False




