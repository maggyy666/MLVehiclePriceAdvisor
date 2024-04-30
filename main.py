import csv
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver_path = 'C:\\Users\\kczyz\\PycharmProjects\\KayakWebScraper\\chromedriver.exe'
csv_directory = 'C:\\Users\\kczyz\\PycharmProjects\\KayakWebScraper\\CSV_FILES'

chrome_options = Options()
chrome_options.add_argument("--headless")

driver = webdriver.Chrome()
car_count = 1
base_url = "https://www.otomoto.pl/osobowe/"
limit_pages = 8000
csv_data_file = 'data.csv'

car_brands = ["Abarth","Acura","Aiways","Aixam","Alfa-Romeo",
              "Alpine","Aston-Martin","Audi","Austin",
             "Baic","Bentley","BMW","Alpina",
              "Brilliance","Bugatti","Buick","BYD","Cadillac",
              "Casalini","Caterham","Chatenet",
              "Chevrolet","Chrysler","Citroen","Cupra","Dacia","Daewoo",
              "Daihatsu","DeLorean","DFSK","DKW","Dodge",
              "DS-Automobiles","e-go","Elaris","FAW","Ferrari",
              "Fiat","Ford","Gaz","Geely","Genesis","GMC","GWM",
              "Honda","Hongqi","Hummer","Hyundai","iamelectric",
              "Ineos","Infinity","Inny","Isuzu","Iveco","Jaguar",
              "Jeep","Jetour","Kia","KTM","Lada","Lamborghini",
              "Lancia","Land-Rover","Lexus","Ligier",
              "Lincoln","Lotus","Lucid","lynk-and-co",
              "MAN","Maserati","Maxus","Maybach","Mazda","McLaren",
              "Mercedes-Benz","Mercury","MG","Microcar","MINI","Mitsubishi",
              "Morgan","Nissan","Nysa","Oldsmobile","Opel","Peugeot",
              "Plymouth","Polestar","Polonez","Pontiac","Porsche",
              "RAM","Renault","Rolls-Royce","Rover","Saab","Seat","Seres",
              "Skoda","Skywell","Smart","SsangYoung","Subaru","Suzuki","Syrena","Tarpan",
              "Tata","Tesla","Toyota","Trabant","Triumph","Uaz","Vauxhall","VELEX","Volkswagen",
              "Volvo","Warszawa","Wartburg","Wolga","Zastava","ZEEKR","Zuk"]

car_id = 1

try:
    # Open data.csv for main data
    with open(csv_data_file, 'a', newline='', encoding='utf-8') as data_file:
        writer_data = csv.writer(data_file)

        for car_brand in car_brands:
            brand_data = []
            brand_csv_file = os.path.join(csv_directory, f'{car_brand}.csv')

            if os.path.exists(brand_csv_file):
                print(f"Plik CSV dla marki {car_brand} już istnieje. Pomijanie...")
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

                print(f"Liczba ogłoszeń dla {fuel_type.capitalize()}: {count} dla {car_brand.capitalize()}")

                for current_page in range(1, (count // 32) + 2):
                    print(f"Scraping page {current_page} for {car_brand.capitalize()} and fuel type {fuel_type.capitalize()}")

                    if current_page > 1:
                        url = f"{base_url}{car_brand}?search%5Bfilter_enum_fuel_type%5D={fuel_type}&page={current_page}"
                        driver.get(url)
                        WebDriverWait(driver, 10).until(
                            EC.visibility_of_element_located((By.XPATH, './/h3[@class="e1i3khom16 ooa-1n2paoq er34gjf0"]')))
                        time.sleep(2)

                    articles = driver.find_elements(By.CSS_SELECTOR, 'article[class*="ooa-yca59n e1i3khom0"]')

                    for article in articles:
                        data_id = article.get_attribute('data-id')
                        #Creating an exception for brands that have dual-word names
                        brand_mapping ={
                            "Aston": "Aston Martin",
                            "Alfa": "Alfa Romeo",
                            "DS": "DS Automobiles",
                            "Lynk": "Lynk & Co",
                            "Land": "Land Rover"
                        }
                        try:
                            link_element = article.find_element(By.XPATH,'.//a[@target="_self"]')
                            car_name = link_element.text
                            brand_prefix,car_model = car_name.split(" ",1)
                            brand_name = brand_mapping.get(brand_prefix, brand_prefix)
                            car_model = car_model.replace(brand_prefix, "").replace("Martin", "").replace("Romeo","").replace("Automobiles", "").replace(" & Co", "").replace("Rover", "").strip()
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

                        try:
                            dl_mileage_element = article.find_element(By.XPATH,
                                                                      './/dl[@class="ooa-1uwk9ii e1i3khom11"]')
                            mileage_element = dl_mileage_element.find_element(By.XPATH,
                                                                              './/dd[@data-parameter="mileage"]')
                            mileage = mileage_element.text
                        except:
                            mileage = 'null'

                        try:
                            dl_fuel_element = article.find_element(By.XPATH,
                                                                   './/dl[@class="ooa-1uwk9ii e1i3khom11"]')
                            fuel_element = dl_fuel_element.find_element(By.XPATH,
                                                                         './/dd[@data-parameter="fuel_type"]')
                            fuel = fuel_element.text
                        except:
                            fuel = 'null'

                        try:
                            dl_gearbox_element = article.find_element(By.XPATH,
                                                                       './/dl[@class="ooa-1uwk9ii e1i3khom11"]')
                            gearbox_element = dl_gearbox_element.find_element(By.XPATH,
                                                                             './/dd[@data-parameter="gearbox"]')
                            gearbox = gearbox_element.text
                        except:
                            gearbox = 'null'

                        try:
                            dl_year_element = article.find_element(By.XPATH,
                                                                   './/dl[@class="ooa-1uwk9ii e1i3khom11"]')
                            year_element = dl_year_element.find_element(By.XPATH,
                                                                         './/dd[@data-parameter="year"]')
                            year = year_element.text
                        except:
                            year = 'null'

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

                        brand_data.append(
                            [data_id, car_id, brand_name, car_model, mileage, price_pln_formatted, price_eur_formatted,
                             engine_power, gearbox, year, fuel, horse_power, current_page])
                        print("-" * 30)
                        print(f"ID: {data_id}")
                        print(f"Brand: {brand_name}")
                        print(f"Model:{car_model}")
                        print(f"Power:{engine_power} {horse_power} KM")
                        print(f"Mileage: {mileage}")
                        print(f"Fuel_Type: {fuel}")
                        print(f"GearBox: {gearbox}")
                        print(f"Year: {year}")
                        print(f"Price: {price_pln_formatted} PLN / {price_eur_formatted} EUR")
                        print("-" * 30)
                        car_id += 1
                        car_count += 1


                    if current_page % 100 == 0 or current_page == (count // 32) + 1:
                        # Zapisz dane do pliku CSV dla danej marki
                        with open(brand_csv_file, 'a', newline='', encoding='utf-8') as brand_file:
                            writer_brand = csv.writer(brand_file)
                            if current_page == 10:  # Zapisz nagłówki tylko raz na początku
                                writer_brand.writerow(
                                    ["Car_ID", "ID", "Brand", "Model", "Mileage", "Price [PLN]", "Price [EUR]", "Engine_Power",
                                     "GearBox", "Year", "Fuel_Type", "Horse_Power", "On_Page"])
                            for data_row in brand_data:
                                writer_brand.writerow(data_row)

                            print(f"Dane dla marki {car_brand} zostały zapisane do pliku {brand_csv_file}")

                        # Wyczyść dane dla danej marki, aby nie powielać ich w pliku data.csv
                        brand_data = []

            # Jeśli istnieje plik CSV dla danej marki, dodaj dane do pliku danych
            if os.path.exists(brand_csv_file):
                with open(csv_data_file, 'a', newline='', encoding='utf-8') as data_file:
                    writer_data = csv.writer(data_file)
                    with open(brand_csv_file, 'r', newline='', encoding='utf-8') as brand_csv:
                        reader_brand = csv.reader(brand_csv)
                        next(reader_brand)  # Skip header
                        for row in reader_brand:
                            writer_data.writerow(row)

except Exception as e:
    print(f"Error: {e}")

finally:
    driver.quit()
