# MLVehiclePriceAdvisor
![MLVehiclePriceAdvisor (2)](https://github.com/maggyy666/MLVehiclePriceAdvisor/assets/119632961/b2d33b85-4c0a-4d9d-a622-37b3525705f3)
## Introduction
MLVehiclePriceAdvisor is a Python-based web scraper designed to extract vehicle data from the popular automotive marketplace Otomoto. The extracted dataset is then preprocessed and prepared for machine learning (ML) analysis. The project utilizes a random forest ML model to predict optimal pricing for vehicles based on their features.

## Features
- Web scraping of vehicle data from Otomoto.
- Data preprocessing and cleaning for ML analysis.
- Implementation of a random forest ML model for price prediction.
- Console application for user input of vehicle details and receiving optimal pricing recommendations.

## Installation
To use MLVehiclePriceAdvisor, follow these steps:

1. Clone the repository: `git clone https://github.com/maggyy666/MLVehiclePriceAdvisor`
2. Install the required dependencies:
3. `pip install -r requirements.txt`
4. Run the console application:
`python main.py`

## Usage
Note: Before proceeding, make sure to download the ChromeDriver corresponding to your Chrome browser version and place it in your project directory.
### Step 1: Web Scraping with OTOMOTOWebScraper.py
First, the user performs web scraping from OTOMOTO website, using the `OTOMOTOWebScraper.py` script. This script extracts vehicle data and saves each brand's data into separate CSV files, such as `BMW.csv` or `Audi.csv`. The records are saved in the following format:

`[   data_id, car_id, brand_name, car_model, mileage, price_pln_formatted, price_eur_formatted,
                             engine_power, gearbox, year, fuel, horse_power, current_page  ]`

To run the scraper: `python OTOMOTOWebScraper.py`

### Step 2: Data Processing with data_processing.py
Next, process the extracted data using the `data_processing.py` script. This script merges all CSV files, from the specified input folder, applies data preprocessing and cleaning operations, and formats the data for machine learning analysis. The processed data is saved in the `output.csv` file.

To execute the data processing:
`python data_processing.py`

### Step 3: Model Training and Evaluation
After processing the data, train the machine learning model to predict optimal pricing for vehicles based on their features. Use the `RandomForest_Training.py` script to train the Random Forest Machine Learning model and evaluate it's performance using metrics such as squared error.

To train the model and evaluate performance:
`python RandomForest_Training.py`

### Step 4: User Interface with main.py
Once the model is trained, use the console application implemented in the `main.py` script to input vehicle details and recieve optimal pricing recommendations. Follow the prompts in the console to enter the brand name, car model and other relevant information.

To run the console application:
`python main.py`

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
