import os
import csv
import pandas as pd
current_directory = os.getcwd()
data_csv_file = os.path.join(current_directory, 'raw_data.csv')

csv_directory = os.path.join(current_directory, 'CSV_FILES')

csv_files = [file for file in os.listdir(csv_directory) if file.endswith('.csv')]

try:
    with open(data_csv_file, 'a', newline='', encoding='utf-8') as data_file:
        writer_data = csv.writer(data_file)

        for csv_file in csv_files:
            csv_file_path = os.path.join(csv_directory, csv_file)

            if csv_file == 'raw_data.csv':
                continue

            with open(csv_file_path, 'r', newline='', encoding='utf-8') as current_file:
                reader = csv.reader(current_file)

                next(reader)

                for row in reader:
                    writer_data.writerow(row)

    print("Raw data successfully saved to raw_data.csv")

except Exception as e:
    print(f"Error occured while saving data to raw_data.csv file: {e}")

def clean_data(csv_file):
    df = pd.read_csv(csv_file, header=None)
    df.columns = ['data_id', 'car_id', 'brand_name', 'car_model', 'mileage',
                  'price_pln_formatted', 'price_eur_formatted', 'engine_power',
                  'gearbox', 'year', 'fuel', 'horse_power', 'current_page']
    df = df.drop(['data_id','car_id','current_page'], axis=1)
    df['mileage'] = df['mileage'].str.replace(' km', '')
    df['horse_power'] = df['horse_power'].str.replace(' KM', '')
    df['engine_power'] = df['engine_power'].str.replace(' cm3', '')
    df = df.dropna()
    df = df[df['horse_power'].str.match('^\d+$')]
    df.to_csv('cleaned_data.csv', index = False)
    print("Success")
clean_data('raw_data.csv')
