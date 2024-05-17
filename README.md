# MLVehiclePriceAdvisor

## Introduction
MLVehiclePriceAdvisor is a Python-based web scraper designed to extract vehicle data from the popular automotive marketplace Otomoto. The extracted dataset is then preprocessed and prepared for machine learning (ML) analysis. The project utilizes a random forest ML model to predict optimal pricing for vehicles based on their features.

## Features
- Web scraping of vehicle data from Otomoto.
- Data preprocessing and cleaning for ML analysis.
- Implementation of a random forest ML model for price prediction.
- Console application for user input of vehicle details and receiving optimal pricing recommendations.

## Installation
To use MLVehiclePriceAdvisor, follow these steps:

1. Clone the repository:
git clone https://github.com/maggyy666/MLVehiclePriceAdvisor
2. Install the required dependencies:
pip install -r requirements.txt
3. Run the console application:
python main.py

## Usage
### Step 1: Web Scraping with OTOMOTOWebScraper.py
First, the user performs web scraping from OTOMOTO website, using the 'OTOMOTOWebScraper.py' script. This script extracts hevicle data and saves each brand's data into separate CSV files, such as 'BMW.csv' or 'Audi.csv'. The records are saved in the following format:

[   *data_id, car_id, brand_name, car_model, mileage, price_pln_formatted, price_eur_formatted,
                             engine_power, gearbox, year, fuel, horse_power, current_page*  ]

To run the scraper: ***python OTOMOTOWebScraper.py***

### Step 2: Merging CSV Files *with merge_csv_files.py*
Next, the user can use the code in the 'merge_csv_files.py' script to consolidate all data from the separate brand CSV files into a single 'raw_data.csv' file located in the 'dataset_files' folder. The reason for keeping data in separate files initially is to facilitate easier statistical analysis for each brand in the future.

To merge the CSV files:

python merge_csv_files.py


## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
