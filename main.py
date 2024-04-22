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

driver.get("https://www.kayak.pl/explore/KRK-anywhere/20240424,20240501")


base_city = '/html/body/div[2]/div[1]/main/div[2]/div[2]/div[2]/div/div[2]/div/div/div/div[4]/div[1]/div/div[{x}]/div/button/div/div[2]/div[1]/div[1]'
base_price = '/html/body/div[2]/div[1]/main/div[2]/div[2]/div[2]/div/div[2]/div/div/div/div[4]/div/div/div[{x}]/div/button/div/div[2]/div[1]/div[2]'

wait = WebDriverWait(driver,10)
try:
    reject_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="portal-container"]/div/div[2]/div/div/div[3]/div/div[1]/button[3]/div/div')))
    reject_button.click()
    print("Privacy message rejected")
except Exception as e:
    print(f"Error")

wait = WebDriverWait(driver, 50)
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