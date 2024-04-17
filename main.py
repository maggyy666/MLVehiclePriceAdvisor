from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time


driver_path = 'C:\\Users\\kczyz\\PycharmProjects\\ImageDownloader\\chromedriver.exe'

chrome_options = Options()
chrome_options.add_argument("--headless")

service = Service(executable_path=driver_path)
driver = webdriver.Chrome(service=service,options=chrome_options)

driver.get("https://www.kayak.pl/explore/KRK-anywhere/20240424,20240501")
page_text = driver.find_element(By.TAG_NAME, 'body').text

wait = WebDriverWait(driver,10)
