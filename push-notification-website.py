import http.client
import urllib
import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager

# Load environment variables
load_dotenv()

APP_TOKEN = os.getenv("APP_TOKEN")
USER_KEY = os.getenv("USER_KEY")

url = ""

def check_element(url, timeout=10):
    # Set up Selenium with Chrome using webdriver-manager
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Run in headless mode
    chrome_options.add_argument('--disable-gpu')  # Disable GPU for headless mode
    chrome_options.add_argument('--no-sandbox')  # For environments with restricted access
    
    # Automatically manage the ChromeDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    try:
        driver.get(url)

        # Wait dynamically for the presence of the element
        try:
            WebDriverWait(driver, timeout).until(
                EC.presence_of_element_located((By.CLASS_NAME, "event-restriction"))
            )
            print('<div class="event-restriction"> element(s) found on the page.')
            return True  # Element found
        except TimeoutException:
            print('No <div class="event-restriction"> elements were found on the page within the timeout.')
            return False  # No elements found
    finally:
        driver.quit()

# Check the element and send a notification based on the result
if check_element(url):
    conn = http.client.HTTPSConnection("api.pushover.net:443")
    conn.request("POST", "/1/messages.json",
    urllib.parse.urlencode({
        "token": APP_TOKEN,
        "user": USER_KEY,
        "message": "Scottish Rugby tickets not on sale.",
    }), { "Content-type": "application/x-www-form-urlencoded" })
    conn.getresponse()
else:
    quit()
