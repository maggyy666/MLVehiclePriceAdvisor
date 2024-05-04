import os
import csv

csv_directory = 'C:\\Users\\kczyz\\PycharmProjects\\KayakWebScraper\\CSV_FILES'

data_csv_file = os.path.join(csv_directory, 'data.csv')

csv_files = [file for file in os.listdir(csv_directory) if file.endswith('.csv')]

try:
    with open(data_csv_file, 'a', newline='', encoding='utf-8') as data_file:
        writer_data = csv.writer(data_file)

        for csv_file in csv_files:
            csv_file_path = os.path.join(csv_directory, csv_file)

            if csv_file == 'data.csv':
                continue

            with open(csv_file_path, 'r', newline='', encoding='utf-8') as current_file:
                reader = csv.reader(current_file)

                next(reader)

                for row in reader:
                    writer_data.writerow(row)

    print("Dane zostały pomyślnie dodane do pliku data.csv.")

except Exception as e:
    print(f"Wystąpił błąd podczas dodawania danych do pliku data.csv: {e}")
