import os
import pandas as pd
import csv

def merge_csv_files(input_folder, output_file):
    all_files = [f for f in os.listdir(input_folder) if f.endswith('.csv')]
    all_data_frames = []

    for file in all_files:
        file_path = os.path.join(input_folder, file)
        df = pd.read_csv(file_path)
        all_data_frames.append(df)

    merged_df = pd.concat(all_data_frames, ignore_index=True)
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    merged_df.to_csv(output_file, index=False)
    print(f"All CSV files have been merged into {output_file}")

def remove_invalid_horse_power(input_file, output_file):
    with open(input_file, 'r', newline='', encoding='utf-8') as input_csv:
        with open(output_file, 'w+', newline='', encoding='utf-8') as output_csv:
            reader = csv.reader(input_csv)
            writer = csv.writer(output_csv)

            headers = next(reader)
            columns_to_keep = [index for index, header in enumerate(headers) if header not in ["data_id", "car_id", "current_page"]]
            new_headers = [headers[index] for index in columns_to_keep]
            writer.writerow(new_headers)

            for row in reader:
                new_row = [row[index] for index in columns_to_keep]
                horse_power = new_row[9]
                if horse_power.endswith(' KM'):
                    writer.writerow(new_row)

def remove_units(output_file):
    df = pd.read_csv(output_file)
    df['mileage'] = df['mileage'].str.replace(' km','')
    df['engine_power'] = df['engine_power'].str.replace(' cm3','')
    df['horse_power']=df['horse_power'].str.replace(' KM','')

    df['price_pln_formatted'] = df['price_pln_formatted'].str.replace(',', '').astype(float)
    df['price_eur_formatted'] = df['price_eur_formatted'].str.replace(',', '').astype(float)

    df.to_csv(output_file, index=False)

def convert_to_float(input_output_file):
    df = pd.read_csv(input_output_file)

    # rmv if df contains 'km'
    df = df[~df['engine_power'].str.contains('KM')]

    # rmv empty
    df.dropna(subset=['mileage', 'price_pln_formatted', 'price_eur_formatted', 'engine_power'], inplace=True)

    # Usunięcie spacji w kolumnie "engine_power" i konwersja do float
    df['engine_power'] = df['engine_power'].str.replace(' ','').astype(float)

    # rmv km, conv => float
    df['mileage'] = df['mileage'].str.replace(' km','').str.replace(' ','').astype(float)

    # Convert to float
    df['price_pln_formatted'] = df['price_pln_formatted'].astype(float)
    df['price_eur_formatted'] = df['price_eur_formatted'].astype(float)

    # Remove horsepower
    df['horse_power'] = df['horse_power'].str.replace(' KM','')

    df.to_csv(input_output_file, index=False)

def remove_brands_below_treshhold(file,threshold=49):
    df = pd.read_csv(file)
    brand_counts = df['brand_name'].value_counts()
    brands_below_treshold = brand_counts[brand_counts < threshold].index.tolist()

    df = df[~df['brand_name'].isin(brands_below_treshold)]
    df.to_csv(file,index=False)

def balance_data(file):
    data = pd.read_csv(file)
    counts = data['brand_name'].value_counts()
    for brand, count in counts.items():
        if count < 500:
            #x = 3x
            oversampled_data = data[data['brand_name'] == brand].sample(n=3 * count, replace=True)
            data = pd.concat([data, oversampled_data], ignore_index=True)
        elif 500 <= count < 1000:
            # x = 2x
            oversampled_data = data[data['brand_name'] == brand].sample(n=2 * count, replace=True)
            data = pd.concat([data, oversampled_data], ignore_index=True)
        elif 1000 <= count < 3000:
            #x = 1.5x
            oversampled_data = data[data['brand_name'] == brand].sample(n=int(1.5 * count), replace=True)
            data = pd.concat([data, oversampled_data], ignore_index=True)
        elif count >= 3000:
            #x = 1.5x
            oversampled_data = data[data['brand_name'] == brand].sample(n=int(1.5 * count), replace=True)
            data = pd.concat([data, oversampled_data], ignore_index=True)
        data.to_csv(file, index=False)


project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
raw_data = os.path.join(project_dir, 'dataset_files', 'raw_data.csv')
output = os.path.join(project_dir, 'dataset_files', 'output.csv')

input_folder = os.path.join(project_dir, 'CSV_FILES')

if __name__ == "__main__":
    merge_csv_files(input_folder, raw_data)
    remove_invalid_horse_power(raw_data, output)
    remove_units(output)
    convert_to_float(output)
    remove_brands_below_treshhold(output)
    balance_data(output)
