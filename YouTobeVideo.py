import pyautogui
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchWindowException, NoSuchElementException
from datetime import datetime, timedelta
from config import download_path,gecko_driver_path,firefox_binary_path


async def download_video_youtube(input_string):
    # Set Firefox options to include the binary location
    options = Options()
    options.binary_location = firefox_binary_path
    # Set preferences for downloading files
    options.set_preference("browser.download.folderList", 2)  # 2 means custom location
    options.set_preference("browser.download.dir", download_path)
    options.set_preference("browser.helperApps.neverAsk.saveToDisk", "video/mp4")  # Set MIME type for video
    options.set_preference("browser.download.manager.showWhenStarting", False)  # Disable download manager popup
    options.set_preference("pdfjs.disabled", True)  # Disable built-in PDF viewer, if needed
    options.set_preference("browser.download.useDownloadDir", True)  # Ensure downloads use the directory set

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

    # Wait for the page to process
    link_text = 'Download'
    max_retries = 6
    retries = 0

    while retries < max_retries:
        try:
            # Attempt to click the Download link
            WebDriverWait(driver, 1).until(
                EC.element_to_be_clickable((By.LINK_TEXT, link_text))
            ).click()
            print(f'Try {retries + 1}: Download link clicked')

            # Wait for the new tab to open
            WebDriverWait(driver, 5).until(
                EC.number_of_windows_to_be(2)
            )
            print('New tab opened, proceeding with download...')
            break  # Exit the loop if successful

        except TimeoutException:
            retries += 1
            print(f'Try {retries}: Failed, retrying...')

    # If the max retries are reached without success
    if retries == max_retries:
        print('Max retries reached. Unable to click the download link or open a new tab.')

    # Continue with the rest of the process if successful
    if retries < max_retries:
        time.sleep(2)
        print('Checking for video element...')

        original_window = driver.current_window_handle

        # Wait for the new tab to be opened and switch to it
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
            time.sleep(1)  # Wait for the context menu to appear

            # Using PyAutoGUI to simulate pressing the keyboard keys to trigger "Save As"
            for _ in range(5):
                pyautogui.press('up')  # Navigate to Save As
            pyautogui.press('enter')  # Trigger Save As
            time.sleep(2)
            pyautogui.press('enter')

            print('Save As initiated')

            time.sleep(10)
            driver.close()
        except TimeoutException:
            print("No video element found. Executing alternative logic...")
            # Alternative logic when no video is found
            time.sleep(10)
            driver.close()
