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

                    try:
                        # Mileage
                        dl_mileage_element = article.find_element(By.XPATH, './/dl[@class="ooa-1uwk9ii e1i3khom11"]')
                        mileage_element = dl_mileage_element.find_element(By.XPATH, './/dd[@data-parameter="mileage"]')
                        mileage = mileage_element.text
                    except:
                        mileage = 'null'
                    try:
                        # Type_Of_Fuel
                        dl_fuel_element = article.find_element(By.XPATH, './/dl[@class="ooa-1uwk9ii e1i3khom11"]')
                        fuel_element = dl_fuel_element.find_element(By.XPATH, './/dd[@data-parameter="fuel_type"]')
                        fuel = fuel_element.text
                    except:
                        fuel = 'null'
                    try:
                        # Gearbox
                        dl_gearbox_element = article.find_element(By.XPATH, './/dl[@class="ooa-1uwk9ii e1i3khom11"]')
                        gearbox_element = dl_gearbox_element.find_element(By.XPATH, './/dd[@data-parameter="gearbox"]')
                        gearbox = gearbox_element.text
                    except:
                        gearbox = 'null'

                    try:
                        # Year
                        dl_year_element = article.find_element(By.XPATH, './/dl[@class="ooa-1uwk9ii e1i3khom11"]')
                        year_element = dl_year_element.find_element(By.XPATH, './/dd[@data-parameter="year"]')
                        year = year_element.text
                    except:
                        year = 'null'

                    try:
                        # Price
                        price_element = article.find_element(By.XPATH,
                                                             './/h3[@class="e1i3khom16 ooa-1n2paoq er34gjf0"]')
                        price = price_element.text
                    except:
                        price = 'null'

                    try:
                        # Currency
                        currency_element = article.find_element(By.XPATH,
                                                                './/p[@class="e1i3khom17 ooa-8vn6i7 er34gjf0"]')
                        currency = currency_element.text
                    except:
                        currency = 'null'

                    writer.writerow(
                        [car_id, car_name, mileage, price, currency, engine_power, horse_power, current_page])

                    print("-" * 30)
                    print(f"ID: {data_id}")
                    print(f"Name: {car_name}")
                    print(f"Power:{engine_power} {horse_power} KM")
                    print(f"Mileage: {mileage}")
                    print(f"Fuel_Type: {fuel}")
                    print(f"GearBox: {gearbox}")
                    print(f"Year: {year}")
                    print(f"Price: {price} {currency}")
                    print("-" * 30)
                    car_id += 1
                    if car_id % 32 == 0:
                        current_page += 1
                try:
                    count_element = driver.find_element(By.XPATH, '//p[@class="e17gkxda2 ooa-17owgto er34gjf0"]/b')
                    count = int(count_element.text.replace(" ", ""))
                except:
                    count = 0

                fuel_counts[fuel_type] = count
                print(f"Liczba ogłoszeń dla {fuel_type.capitalize()}: {count}")

            groups = [
                (fuel_counts["hybrid"], "?search%5Bfilter_enum_fuel_type%5D=hybrid"),
                (fuel_counts["electric"], "?search%5Bfilter_enum_fuel_type%5D=electric"),
                (fuel_counts["petrol"], "?search%5Bfilter_enum_fuel_type%5D=petrol"),
                (fuel_counts["diesel"], "?search%5Bfilter_enum_fuel_type%5D=diesel"),
                (fuel_counts["gas"], "?search%5Bfilter_enum_fuel_type%5D=gas"),
                (fuel_counts["ethanol"], "?search%5Bfilter_enum_fuel_type%5D=ethanol"),
                (fuel_counts["hydrogen"], "?search%5Bfilter_enum_fuel_type%5D=hydrogen"),
                (fuel_counts["petrol-cng"], "?search%5Bfilter_enum_fuel_type%5D=petrol-cng"),
                (fuel_counts["petrol-lpg"], "?search%5Bfilter_enum_fuel_type%5D=petrol-lpg"),
            ]

            for group_count, filter_param in groups:
                current_page = 1
                while (current_page - 1) * 32 < group_count:
                    print(f"Scraping page {current_page} for {car_brand.capitalize()}")

                    if filter_param:
                        url = f"{base_url}{car_brand}{filter_param}&page={current_page}"
                    else:
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
                            parts = car_name.split(" ",1)
                            if parts[0] == "Aston":
                                brand_name = "Aston Martin"
                                car_model = parts[1].replace("Martin","").strip()
                            elif parts[0] == "Alfa":
                                brand_name = "Alfa Romeo"
                                car_model = parts[1].replace("Romeo","").strip()
                            elif parts[0] == "DS":
                                brand_name = "DS Automobiles"
                                car_model = parts[1].replace("Automobiles","").strip()
                            elif parts[0] == "Lynk":
                                brand_name = "Lynk & Co"
                                car_model = parts[1].replace(" & Co","").strip()
                            elif parts[0] == "Land":
                                brand_name = "Land Rover"
                                car_model = parts[1].replace("Rover","").strip()

                            else:
                                brand_name = parts[0]
                                car_model = parts[1]
                        except:
                            car_name = 'null'

                        try:
                            # Power
                            power_element = article.find_element(By.XPATH,
                                                                 './/p[@class="e1i3khom10 ooa-1tku07r er34gjf0"]')
                            power_text = power_element.text
                            split = power_text.split("•")
                            engine_power = split[0].strip()
                            horse_power = split[1].strip().split("•")[0].strip()
                        except:
                            engine_power = 'null'
                            horse_power = 'null'

                        try:
                            # Mileage
                            dl_mileage_element = article.find_element(By.XPATH,
                                                                      './/dl[@class="ooa-1uwk9ii e1i3khom11"]')
                            mileage_element = dl_mileage_element.find_element(By.XPATH,
                                                                              './/dd[@data-parameter="mileage"]')
                            mileage = mileage_element.text
                        except:
                            mileage = 'null'
                        try:
                            # Type_Of_Fuel
                            dl_fuel_element = article.find_element(By.XPATH, './/dl[@class="ooa-1uwk9ii e1i3khom11"]')
                            fuel_element = dl_fuel_element.find_element(By.XPATH, './/dd[@data-parameter="fuel_type"]')
                            fuel = fuel_element.text
                        except:
                            fuel = 'null'
                        try:
                            # Gearbox
                            dl_gearbox_element = article.find_element(By.XPATH,
                                                                      './/dl[@class="ooa-1uwk9ii e1i3khom11"]')
                            gearbox_element = dl_gearbox_element.find_element(By.XPATH,
                                                                              './/dd[@data-parameter="gearbox"]')
                            gearbox = gearbox_element.text
                        except:
                            gearbox = 'null'

                        try:
                            # Year
                            dl_year_element = article.find_element(By.XPATH, './/dl[@class="ooa-1uwk9ii e1i3khom11"]')
                            year_element = dl_year_element.find_element(By.XPATH, './/dd[@data-parameter="year"]')
                            year = year_element.text
                        except:
                            year = 'null'

                        try:
                            # Price
                            price_element = article.find_element(By.XPATH,
                                                                 './/h3[@class="e1i3khom16 ooa-1n2paoq er34gjf0"]')
                            price = price_element.text
                        except:
                            price = 'null'

                        try:
                            # Currency
                            currency_element = article.find_element(By.XPATH,
                                                                    './/p[@class="e1i3khom17 ooa-8vn6i7 er34gjf0"]')
                            currency = currency_element.text
                        except:
                            currency = 'null'

                        writer.writerow(
                            [data_id,car_id, brand_name,car_model, mileage, price, currency, engine_power,gearbox,year,fuel, horse_power, current_page])

                        print("-" * 30)
                        print(f"ID: {data_id}")
                        print(f"Brand: {brand_name}")
                        print(f"Model:{car_model}")
                        print(f"Power:{engine_power} {horse_power} KM")
                        print(f"Mileage: {mileage}")
                        print(f"Fuel_Type: {fuel}")
                        print(f"GearBox: {gearbox}")
                        print(f"Year: {year}")
                        print(f"Price: {price} {currency}")
                        print("-" * 30)
                        car_id += 1
                        if car_id % 32 == 0:
                            current_page += 1







except Exception as e:
    print(f"Error: {e}")
finally:
  driver.quit()