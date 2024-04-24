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


    print(f"Scraping page: {current_page}")
    articles = driver.find_elements(By.CSS_SELECTOR, 'article[class*="ooa-yca59n e1i3khom0"]')
    data_ids = []
    for article in articles:
        print(f"Car NO. {id}")
        data_id = article.get_attribute('data-id')
        data_ids.append(data_id)
        link_element = article.find_element(By.XPATH, './/a[@target="_self"]')
        car_name = link_element.text
        # Mileage
        dl_mileage_element = article.find_element(By.XPATH, './/dl[@class="ooa-1uwk9ii e1i3khom11"]')
        mileage_element = dl_mileage_element.find_element(By.XPATH, './/dd[@data-parameter="mileage"]')
        mileage = mileage_element.text
        # Type_Of_Fuel
        dl_fuel_element = article.find_element(By.XPATH, './/dl[@class="ooa-1uwk9ii e1i3khom11"]')
        fuel_element = dl_fuel_element.find_element(By.XPATH, './/dd[@data-parameter="fuel_type"]')
        fuel = fuel_element.text
        # Gearbox
        dl_gearbox_element = article.find_element(By.XPATH, './/dl[@class="ooa-1uwk9ii e1i3khom11"]')
        gearbox_element = dl_gearbox_element.find_element(By.XPATH, './/dd[@data-parameter="gearbox"]')
        gearbox = gearbox_element.text
        # Year
        dl_year_element = article.find_element(By.XPATH, './/dl[@class="ooa-1uwk9ii e1i3khom11"]')
        year_element = dl_year_element.find_element(By.XPATH, './/dd[@data-parameter="year"]')
        year = year_element.text
        print("-" * 30)
        print(f"ID: {data_id}")
        print(f"Name: {car_name}")
        print(f"Mileage: {mileage}")
        print(f"Fuel_Type: {fuel}")
        print(f"GearBox: {gearbox}")
        print(f"Year: {year}")
        print("-" * 30)
        id += 1
except Exception as e:
        print(f"Error for path {current_city}: {e}")



driver.quit()