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

def download_video_youtube(input_string):
    options = Options()
    options.binary_location = firefox_binary_path
    options.set_preference("browser.download.folderList", 2)
    options.set_preference("browser.download.dir", download_path)
    options.set_preference("browser.helperApps.neverAsk.saveToDisk", "video/mp4")
    options.set_preference("browser.download.manager.showWhenStarting", False)
    options.set_preference("pdfjs.disabled", True)
    options.set_preference("browser.download.useDownloadDir", True)

    # Initialize the Firefox WebDriver
    service = Service(gecko_driver_path)
    driver = webdriver.Firefox(service=service, options=options)

    # Open the website
    driver.get('https://www.y2mate.com.cn/en')
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, 'txt-url'))
    )
    print('opened')

    # Find the input element and enter the YouTube URL
    input_element = driver.find_element(By.ID, 'txt-url')
    input_element.send_keys(input_string)

    # Find and click the submit button
    button = driver.find_element(By.ID, 'btn-submit')
    button.click()
    print('submitted')

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




