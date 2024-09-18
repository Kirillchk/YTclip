import pyautogui
import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchWindowException, NoSuchElementException
from datetime import datetime, timedelta
from config import download_path, gecko_driver_path, firefox_binary_path


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

    link_text = 'Download'
    max_retries = 12
    retries = 0

    while retries < max_retries:
        try:
            WebDriverWait(driver, 1).until(
                EC.element_to_be_clickable((By.LINK_TEXT, link_text))
            ).click()
            print(f'Try {retries + 1}: Download link clicked')

            WebDriverWait(driver, 5).until(
                EC.number_of_windows_to_be(2)
            )
            print('New tab opened, proceeding with download...')
            break

        except TimeoutException:
            retries += 1
            print(f'Try {retries}: Failed, retrying...')

    if retries == max_retries:
        print('Max retries reached. Unable to click the download link or open a new tab.')

    if retries < max_retries:
        time.sleep(2)
        print('Checking for video element...')

        original_window = driver.current_window_handle

        for handle in driver.window_handles:
            if handle != original_window:
                try:
                    driver.switch_to.window(handle)
                    print("Switched to the new tab.")
                except NoSuchWindowException:
                    print("Failed to switch to the new tab, the window might have been closed.")
                    driver.quit()
                    exit()

                break

        # Check if the video element exists in the newly opened tab
        try:
            video_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, 'video'))
            )
            print('Video element found, proceeding with download...')

            # Execute JavaScript to create a download link for the video and click it
            actions = ActionChains(driver)
            actions.context_click(video_element).perform()
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
                driver.close()
            else:
                print("Not downloaded")
                driver.close()
        except TimeoutException:
            print("No video element found. Executing alternative logic...")
            # Alternative logic when no video is found
            is_downloaded = wait_for_download(download_path)
            if is_downloaded:
                print("Downloaded successfully")
                driver.close()
            else:
                print("Not downloaded")
                driver.close()


def wait_for_download(path, timeout=60):
    end_time = time.time() + timeout
    while time.time() < end_time:
        files = os.listdir(path)
        if any(file.endswith(".mp4") for file in files):
            print("Download completed.")
            return True
        time.sleep(1)
    print("Download did not complete in the given time.")
    return False
