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
    with open(csv_file, 'w',newline='',encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Car_ID. ","ID", "Nazwa pojazdu", "Przebieg", "Cena", "Waluta", "Engine_Power", "On_Page"])

        for car_brand in car_brands:
            current_page = 1
            car_id = 1

            url_count =f"{base_url}{car_brand}"
            driver.get(url_count)

            try:
                count_element = driver.find_element(By.XPATH, '//p[@class="e17gkxda2 ooa-17owgto er34gjf0"]/b')
                count = int(count_element.text.replace(" ",""))
                print(f"Liczba ogloszen dla: {car_brand.capitalize()}: {count}")
            except:
                print(f"Error")
                continue
            if count == 0:
                print(f"Brak ogloszen dla {car_brand.capitalize()}")
                continue


            while car_id <= count and (current_page-1)*32 < count:
                print(f"Scraping page {current_page} for {car_brand.capitalize()}")
                url = f"{base_url}{car_brand}?page={current_page}"
                driver.get(url)

                articles = driver.find_elements(By.CSS_SELECTOR, 'article[class*="ooa-yca59n e1i3khom0"]')
                data_ids = []

                for article in articles:
                    print(f"Car NO. {car_id}")
                    data_id = article.get_attribute('data-id')
                    data_ids.append(data_id)

                    try:
                        # Car_Name
                        link_element = article.find_element(By.XPATH, './/a[@target="_self"]')
                        car_name = link_element.text
                    except:
                        car_name = 'null'

                    try:
                        # Power
                        power_element = article.find_element(By.XPATH, './/p[@class="e1i3khom10 ooa-1tku07r er34gjf0"]')
                        power_text = power_element.text
                        split = power_text.split("•")
                        engine_power = split[0].strip()
                        horse_power = split[1].strip().split("•")[0].strip()
                    except:
                        engine_power = 'null'
                        horse_power = 'null'

driver.quit()