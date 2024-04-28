from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import csv
import os
import time
from selenium .webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver_path = 'C:\\Users\\kczyz\\PycharmProjects\\ImageDownloader\\chromedriver.exe'

chrome_options = Options()
chrome_options.add_argument("--headless")

driver = webdriver.Chrome()

base_url = "https://www.otomoto.pl/osobowe/"
limit_pages = 8000
current_page = 1
csv_file = 'data.csv'
status_file = 'status.txt'



car_brands = ["bmw"]

car_brands = ["Abarth","Acura","Aiways","Aixam","Alfa-Romeo",
              "Alpine","Asia","Aston-Martin","Austin",
              "Autobianchi","Baic","Bentley","BMW","Alpina",
              "Brilliance","Bugatti","Buick","BYD","Cadillac",
              "Casalini","Caterham","Cenntro","Changan","Chatenet",
              "Chevrolet","Chrysler","Citroen","Cupra","Dacia","Daewoo",
              "Daihatsu","DeLorean","DFM","DFSK","DKW","Dodge","Doosan",
              "DR-MOTOR","DS-Automobiles","e-go","Elaris","FAW","Ferrari",
              "Fiat","Fisker","Ford","Gaz","Geely","Genesis","GMC","GWM",
              "HiPhi","Honda","Hongqi","Hummer","Hyundai","iamelectric",
              "Ineos","Infinity","Inny","Isuzu","Iveco","JAC","Jaguar",
              "Jeep","Jetour","Jinpeng","Kia","KTM","Lada","Lamborghini",
              "Lancia","Land-Rover","Leapmotor","LEVC","Lexus","Ligier",
              "Lincoln","Lixiang","Lotus","LTI","Lucid","lynk-and-co",
              "MAN","Maserati","MAXIMUS","Maxus","Maybach","Mazda","McLaren",
              "Mercedes-Benz","Mercury","MG","Microcar","MINI","Mitsubishi",
              "Morgan","NIO","Nissan","Nysa","Oldsmobile","Opel","Peugeot",
              "Piaggio","Plymouth","Polestar","Polonez","Pontiac","Porsche",
              "RAM","Renault","Rolls-Royce","Rover","Saab","Seat","Seres","Shuanghuan",
              "Skoda","Skywell","Smart","SsangYoung","Subaru","Suzuki","Syrena","Tarpan",
              "Tata","Tesla","Toyota","Trabant","Triumph","Uaz","Vauxhall","VELEX","Volkswagen",
              "Volvo","Voyah","Warszawa","Wartburg","Wolga","XPeng","Zaporozec","Zastava","ZEEKR","Zuk"]

try:

    with open(csv_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(
            ["Car_ID. ", "ID", "Brand", "Model", "Mileage", "Price [PLN]", "Price [EUR]", "Engine_Power",
             "GearBox", "Year", "Fuel_Type", "Horse_Power", "On_Page"])

        for car_brand in car_brands:
            # Sprawdź, czy plik CSV dla danej marki już istnieje
            if os.path.exists(os.path.join(csv_directory, f'{car_brand}.csv')):
                print(f"Plik CSV dla marki {car_brand} już istnieje. Pomijanie...")
                continue

            # Utwórz nazwę pliku CSV dla danej marki
            csv_brand_file = os.path.join(csv_directory, f'{car_brand}.csv')

            # Otwórz plik CSV dla danej marki do zapisu danych specyficznych dla marki
            with open(csv_brand_file, 'w', newline='', encoding='utf-8') as brand_file:
                writer_brand = csv.writer(brand_file)
                writer_brand.writerow(
                    ["Car_ID", "ID", "Brand", "Model", "Mileage", "Price [PLN]", "Price [EUR]", "Engine_Power",
                     "GearBox", "Year", "Fuel_Type", "Horse_Power", "On_Page"])

            car_id = 1

            fuel_counts = {}

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
                "plugin-hybrid",  # Dodanie nowego rodzaju paliwa
            ]

            for fuel_type in fuel_types:
                url = f"{base_url}{car_brand}?search%5Bfilter_enum_fuel_type%5D={fuel_type}"
                driver.get(url)
                #WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.XPATH, './/h3[@class="e1i3khom16 ooa-1n2paoq er34gjf0"]')))

                try:
                    count_element = driver.find_element(By.XPATH, '//p[@class="e17gkxda2 ooa-17owgto er34gjf0"]/b')
                    count = int(count_element.text.replace(" ", ""))
                except:
                    count = 0

                fuel_counts[fuel_type] = count
                print(f"Liczba ogłoszeń dla {fuel_type.capitalize()}: {count} dla {car_brand.capitalize()}")

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
                (fuel_counts["plugin-hybrid"], "?search%5Bfilter_enum_fuel_type%5D=plugin-hybrid"),  # Dodanie nowego rodzaju paliwa
            ]

            for group_count, filter_param in groups:
                current_page = 1
                while (current_page - 1) * 32 < group_count:
                    print(f"Scraping page {current_page} for {car_brand.capitalize()}")
                    time.sleep(3)
                    if filter_param:
                        url = f"{base_url}{car_brand}{filter_param}&page={current_page}"
                    else:
                        url = f"{base_url}{car_brand}?page={current_page}"

                    driver.get(url)
                    WebDriverWait(driver, 10).until(
                        EC.visibility_of_element_located((By.XPATH, './/h3[@class="e1i3khom16 ooa-1n2paoq er34gjf0"]')))

                    articles = driver.find_elements(By.CSS_SELECTOR, 'article[class*="ooa-yca59n e1i3khom0"]')
                    data_ids = []

                    for article in articles:
                        print(f"Car NO. {car_id}")
                        data_id = article.get_attribute('data-id')
                        data_ids.append(data_id)

                        try:
                            link_element = article.find_element(By.XPATH, './/a[@target="_self"]')
                            car_name = link_element.text
                            parts = car_name.split(" ", 1)
                            if parts[0] == "Aston":
                                brand_name = "Aston Martin"
                                car_model = parts[1].replace("Martin", "").strip()
                            elif parts[0] == "Alfa":
                                brand_name = "Alfa Romeo"
                                car_model = parts[1].replace("Romeo", "").strip()
                            elif parts[0] == "DS":
                                brand_name = "DS Automobiles"
                                car_model = parts[1].replace("Automobiles", "").strip()
                            elif parts[0] == "Lynk":
                                brand_name = "Lynk & Co"
                                car_model = parts[1].replace(" & Co", "").strip()
                            elif parts[0] == "Land":
                                brand_name = "Land Rover"
                                car_model = parts[1].replace("Rover", "").strip()
                            else:
                                brand_name = parts[0]
                                car_model = parts[1]
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
                            dl_fuel_element = article.find_element(By.XPATH, './/dl[@class="ooa-1uwk9ii e1i3khom11"]')
                            fuel_element = dl_fuel_element.find_element(By.XPATH, './/dd[@data-parameter="fuel_type"]')
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
                            dl_year_element = article.find_element(By.XPATH, './/dl[@class="ooa-1uwk9ii e1i3khom11"]')
                            year_element = dl_year_element.find_element(By.XPATH, './/dd[@data-parameter="year"]')
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

                            # Usunięcie spacji i przecinków z ceny, a następnie parsowanie jako float
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


                            # Formatowanie ceny z separatorem tysięcy
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

                        writer.writerow(
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
                    current_page += 1
                    time.sleep(2)
except Exception as e:
    print(f"Error: {e}")
finally:
    driver.quit()
