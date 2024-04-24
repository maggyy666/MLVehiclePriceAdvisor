from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
import requests
from bs4 import BeautifulSoup


driver_path = 'C:\\Users\\kczyz\\PycharmProjects\\ImageDownloader\\chromedriver.exe'

chrome_options = Options()
chrome_options.add_argument("--headless")


driver = webdriver.Chrome()

url = "https://www.otomoto.pl/osobowe"
try:
    for i in range(1, 30):
        current_city = base_city.format(x=i)
        current_price = base_price.format(x=i)

        city_element = wait.until(EC.visibility_of_element_located((By.XPATH, current_city)))
        price_element = wait.until(EC.visibility_of_element_located((By.XPATH, current_price)))

        city_name = city_element.text if city_element.is_displayed() else "Not Visible"
        price_name = price_element.text if price_element.is_displayed() else "Not Visible"

        print(f"{city_name},{price_name}")
        if i == 12:
            load_more_button = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="LWbU-showMoreButton"]/div[1]/div')))
            load_more_button.click()
            time.sleep(2)


except Exception as e:
        print(f"Error for path {current_city}: {e}")



driver.quit()