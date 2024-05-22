import csv
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
driver_path = '' #put your chrome driver directory here
csv_directory = os.path.join(project_dir, 'CSV_FILES')

chrome_options = Options()
chrome_options.add_argument("--headless")

driver = webdriver.Chrome()
car_count = 1
base_url = "https://www.otomoto.pl/osobowe/"
limit_pages = 8000

car_brands = ["Abarth", "Acura", "Aiways", "Aixam", "Alfa-Romeo",
              "Alpine", "Aston-Martin", "Audi", "Austin",
              "Baic", "Bentley", "BMW", "Alpina",
              "Brilliance", "Bugatti", "Buick", "BYD", "Cadillac",
              "Casalini", "Caterham", "Chatenet",
              "Chevrolet", "Chrysler", "Citroen", "Cupra", "Dacia", "Daewoo",
              "Daihatsu", "DeLorean", "DFSK", "DKW", "Dodge",
              "DS-Automobiles", "e-go", "Ferrari",
              "Fiat", "Ford", "Gaz", "Geely", "Genesis", "GMC", "GWM",
              "Honda", "Hongqi", "Hummer", "Hyundai", "iamelectric",
              "Ineos", "Infiniti", "Inny", "Isuzu", "Iveco", "Jaguar",
              "Jeep", "Jetour", "Kia", "KTM", "Lada", "Lamborghini",
              "Lancia", "Land-Rover", "Lexus", "Ligier",
              "Lincoln", "Lotus", "Lucid", "lynk-and-co",
              "MAN", "Maserati", "Maxus", "Maybach", "Mazda", "McLaren",
              "Mercedes-Benz", "Mercury", "MG", "Microcar", "MINI", "Mitsubishi",
              "Morgan", "Nissan", "Nysa", "Oldsmobile", "Opel", "Peugeot",
              "Plymouth", "Polestar", "Polonez", "Pontiac", "Porsche",
              "RAM", "Renault", "Rolls-Royce", "Rover", "Saab", "Seat", "Seres",
              "Skoda", "Skywell", "Smart", "SsangYong", "Subaru", "Suzuki", "Syrena", "Tarpan",
              "Tata", "Tesla", "Toyota", "Trabant", "Triumph", "Uaz", "Vauxhall", "VELEX", "Volkswagen",
              "Volvo", "Marka_Warszawa", "Wartburg", "Wolga", "Zastawa", "ZEEKR", "Zuk"]

car_id = 1

try:
    for car_brand in car_brands:
        brand_csv_file = os.path.join(csv_directory, f'{car_brand}.csv')

        if os.path.exists(brand_csv_file):
            print(f"CSV File for brand: {car_brand} already exists. Skipping...")
            continue

        fuel_types = [
            "hybrid",
            "electric",
            "petrol",
            "diesel",
            "gas",
            "ethanol",
            "hydrogen",
            "petrol-cng",
            "petrol-lpg",
            "plugin-hybrid"
        ]

        for fuel_type in fuel_types:
            url = f"{base_url}{car_brand}?search%5Bfilter_enum_fuel_type%5D={fuel_type}"
            driver.get(url)

            try:
                count_element = driver.find_element(By.XPATH, '//p[@class="e17gkxda2 ooa-17owgto er34gjf0"]/b')
                count = int(count_element.text.replace(" ", ""))
            except:
                count = 0

            print(f"Number of listings {fuel_type.capitalize()}: {count} for {car_brand.capitalize()}")

            for current_page in range(1, (count // 32) + 2):
                print(f"Scraping page {current_page} for {car_brand.capitalize()} and fuel type {fuel_type.capitalize()}")

                if current_page > 1:
                    url = f"{base_url}{car_brand}?search%5Bfilter_enum_fuel_type%5D={fuel_type}&page={current_page}"
                    driver.get(url)
                    WebDriverWait(driver, 30).until(
                        EC.visibility_of_element_located((By.XPATH, './/h3[@class="e1i3khom16 ooa-1n2paoq er34gjf0"]')))
                    time.sleep(2)

                articles = driver.find_elements(By.CSS_SELECTOR, 'article[class*="ooa-yca59n e1i3khom0"]')

                for article in articles:
                    data_id = article.get_attribute('data-id')
                    # Creating an exception for brands that have dual-word names
                    brand_mapping = {
                        "Aston": "Aston Martin",
                        "Alfa": "Alfa Romeo",
                        "DS": "DS Automobiles",
                        "Lynk": "Lynk & Co",
                        "Land": "Land Rover"
                    }
                    try:
                        link_element = article.find_element(By.XPATH, './/a[@target="_self"]')
                        car_name = link_element.text
                        brand_prefix, car_model = car_name.split(" ", 1)
                        brand_name = brand_mapping.get(brand_prefix, brand_prefix)
                        car_model = car_model.replace(brand_prefix, "").replace("Martin", "").replace("Romeo", "").replace(
                            "Automobiles", "").replace(" & Co", "").replace("Rover", "").strip()
                    except:
                        car_name = 'null'
                    try:
                        power_element = article.find_element(By.XPATH,
                                                             './/p[@class="e1i3khom10 ooa-1tku07r er34gjf0"]')
                        power_text = power_element.text
                        split = power_text.split("•")
                        engine_power = split[0].strip()
                        horse_power = split[1].strip().split("•")[0].strip()
                    except:
                        engine_power = 'null'
                        horse_power = 'null'

                    parameters = {
                        "mileage": "null",
                        "fuel_type": "null",
                        "gearbox": "null",
                        "year": "null"
                    }

                    try:
                        dl_elements = article.find_elements(By.XPATH, './/dl[@class="ooa-1uwk9ii e1i3khom11"]')
                        for dl_element in dl_elements:
                            for param, default_value in parameters.items():
                                try:
                                    element = dl_element.find_element(By.XPATH, f'.//dd[@data-parameter="{param}"]')
                                    parameters[param] = element.text
                                except:
                                    pass
                    except:
                        pass

                    mileage = parameters["mileage"]
                    fuel = parameters["fuel_type"]
                    gearbox = parameters["gearbox"]
                    year = parameters["year"]

                    try:
                        price_element = article.find_element(By.XPATH,
                                                             './/h3[@class="e1i3khom16 ooa-1n2paoq er34gjf0"]')
                        price = price_element.text
                        currency_element = article.find_element(By.XPATH,
                                                                 './/p[@class="e1i3khom17 ooa-8vn6i7 er34gjf0"]')
                        currency = currency_element.text

                        # Removing spaces/commas and converting to float
                        price = price.replace(' ', '').replace(',', '')
                        price = float(price)

                        if currency == 'PLN':
                            price_pln = price
                            price_eur = round(price_pln * 0.23, 2)
                        elif currency == 'EUR':
                            price_eur = price
                            price_pln = round(price_eur * 4.32, 2)
                        else:
                            price_pln = 'null'
                            price_eur = 'null'

                        # Formatting price
                        def format_price_with_thousands_separator(price):
                            parts = str(price).split('.')
                            integer_part = '{:,.0f}'.format(int(parts[0]))
                            if len(parts) > 1:
                                return f"{integer_part}.{parts[1]}"
                            else:
                                return integer_part

                        price_pln_formatted = format_price_with_thousands_separator(price_pln)
                        price_eur_formatted = format_price_with_thousands_separator(price_eur)

                    except:
                        price_pln = 'null'
                        price_eur = 'null'
                        currency = 'null'

                    with open(brand_csv_file, 'a', newline='', encoding='utf-8') as brand_file:
                        writer_brand = csv.writer(brand_file)

                        # Sprawdź, czy plik jest pusty
                        if brand_file.tell() == 0:
                            writer_brand.writerow(
                                ["data_id", "car_id", "brand_name", "car_model", "mileage", "price_pln_formatted",
                                 "price_eur_formatted",
                                 "engine_power", "gearbox", "year", "fuel", "horse_power", "current_page"])

                        writer_brand.writerow(
                            [data_id, car_id, brand_name, car_model, mileage, price_pln_formatted, price_eur_formatted,
                             engine_power, gearbox, year, fuel, horse_power, current_page])

                    print("-" * 30)
                    print(f"CAR NO. {car_id} / {count}")
                    print(f"-"*30)
                    print(f"ID: {data_id}")
                    print(f"Brand: {brand_name}")
                    print(f"Model:{car_model}")
                    print(f"Power:{engine_power} {horse_power}")
                    print(f"Mileage: {mileage}")
                    print(f"Fuel_Type: {fuel}")
                    print(f"GearBox: {gearbox}")
                    print(f"Year: {year}")
                    print(f"Price: {price_pln_formatted} PLN / {price_eur_formatted} EUR")
                    car_id += 1
                    car_count += 1

                if current_page % 100 == 0 or current_page == (count // 32) + 1:
                    print(f"Data for a brand: {car_brand} has been successfully scraped into a CSV file: {brand_csv_file}")

except Exception as e:
    print(f"Error: {e}")

finally:
    driver.quit()
