# MLVehiclePriceAdvisor
![MLVehiclePriceAdvisor (2)](https://github.com/maggyy666/MLVehiclePriceAdvisor/assets/119632961/b2d33b85-4c0a-4d9d-a622-37b3525705f3)
## Introduction
MLVehiclePriceAdvisor is a Python-based web scraper designed to extract vehicle data from the popular automotive marketplace Otomoto. The extracted dataset is then preprocessed and prepared for machine learning (ML) analysis. The project utilizes a random forest ML model to predict optimal pricing for vehicles based on their features.

### Mathematical Prerequisites

To understand the concepts used in this project, it's beneficial to have knowledge of the following:

- Basics of statistics and probability theory
- Linear algebra (e.g., matrix operations)
- Machine learning concepts (e.g., regression, ensemble methods)

### Random Forest Prediction

The random forest model predicts the optimal pricing $(\( \hat{y} \))$ for vehicles based on their features $(\( \mathbf{x} \))$. The prediction is calculated as the average of predictions made by individual decision trees:

$$
\hat{y} = \frac{1}{T} \sum_{t=1}^{T} \hat{y}_t(\mathbf{x})
$$

Here, $\( \hat{y}_t(\mathbf{x}) \)$ represents the prediction made by the $\( t \)$-th decision tree in the random forest, and $\( T \)$ is the total number of trees.

## Features
- Web scraping of vehicle data from Otomoto.
- Data preprocessing and cleaning for ML analysis.
- Implementation of a random forest ML model for price prediction.
- Console application for user input of vehicle details and receiving optimal pricing recommendations.

## Installation
To use MLVehiclePriceAdvisor, follow these steps:

1. Clone the repository: `git clone https://github.com/maggyy666/MLVehiclePriceAdvisor`
2. Install the required dependencies: `pip install -r requirements.txt`
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
# Usage
## OTOMOTOWebScraper.py Overview
The `OTOMOTOWebScraper.py` script is a comprehensive tool designed to automate the extraction of vehicle data from the Otomoto website. It leverages the Selenium library to perform web scraping and collects detailed information on various car listings. Below is a detailed breakdown of the script's functionality:
1. **Importing Libraries:** The initial part of the file involves importing necessary libraries such as `csv`, `os`, `time`, and components of the `selenium` module. The `selenium` library is used for automating web browsing using scripts.


2. **Defining Variables:** Various variables are defined, such as `project_dir` (project directory), `driver_path` (path to the browser driver), `csv_directory` (directory where CSV files will be saved), `chrome_options` (Chrome browser options), and `car_brands` (list of car brands to be searched).


3. **Initializing the Browser Driver:** An instance of the Chrome browser driver is created using `webdriver.Chrome()`.


4. **Looping Through Car Brands:** Next, there's an iteration over the list of car brands (`car_brands`) to search for sales listings for each brand. For each brand, the following steps are executed:
- Checking for the existence of a CSV file for the brand. If the file already exists, the search for that brand is skipped.


- For each fuel type (e.g., gasoline, diesel), a URL is constructed containing filtering by brand and fuel type.


- Navigating to the Otomoto website page containing listings for the given brand and fuel type.


- Retrieving the number of available listings for the brand and fuel type.


- Iterating through the pages of listings for the brand and fuel type.


- Extracting data from listings, such as ID, brand, model, engine power, mileage, gearbox type, year of production, price, etc.


- Saving the listing data to a CSV file.

5. **Exception Handling:** In case of an error during the search and data retrieval process, the program will display an error message.

6. **Closing the Browser Driver:** Finally, after searching all car brands, the browser driver is shut down using `driver.quit()`.

### Key Feature

- **Brand-Specific CSV Files:** One of the significant features of this script is that it saves the entire dataset into separate CSV files for each car brand. This organization ensures that data is neatly categorized by brand, making it easier to manage and analyze.

## data_processing.py Overview
This script is an efficient solution for systematically collecting and organizing vehicle listing data from the Otomoto website, facilitating subsequent data analysis and machine learning tasks.

1. **Importing Libraries:**
* The script begins by importing essential libraries such as `os`, `pandas`, and `csv`. Pandas is used for data manipulation and analysis.

2. **Defining Functions:**
* **merge_csv_files(input_folder,output_file):**
  - This function merges multiple CSV files located in the specified input_folder into a single CSV file named `output_file`.
  - It iterates through all CSV files in the folder, reads each file into a DataFrame, and appends the DataFrame to a list.
  - Finally, it concatenates all DataFrames into one and saves the merged DataFrame to the `output_file`.
* **remove_invalid_horse_power(input_file, output_file):**
  - This function removes rows with invalid horsepower values from the `input_file` and saves the cleaned data to the output_file.
  - It skips columns like` data_id`, `car_id`, and` current_page` and retains the rest.
  - Rows where the `horse_power` column does not end with 'KM' are filtered out.
* **remove_units(output_file):**
  - This function removes unit labels from the `mileage`, `engine_power`, and `horse_power` columns in the output_file.
  - It also formats the `price_pln_formatted` and `price_eur_formatted` columns as floats by removing commas.
  - The cleaned data is saved back to the same file.
* **convert_to_float(input_output_file):**
  - This function converts relevant columns to float data type and removes any rows with missing or invalid values.
  - It ensures that columns like` engine_power`, `mileage`, `price_pln_formatted`, and `price_eur_formatted` are properly formatted as floats.
  - It also filters out rows with invalid `engine_power` entries and saves the cleaned data back to the file.
* **remove_brands_below_treshold(file, threshold=49):**
  - This function removes brands that have fewer than a specified threshold of listings.
  - It counts the number of listings for each brand and filters out those below the threshold, saving the cleaned data back to the file.
* **balance_data(file):**
  - This function balances the dataset by oversampling brands that have fewer listings.
  - Depending on the number of listings, it oversamples the data by different factors (e.g., 3x, 2x, 1.5x) to ensure a balanced dataset.
  - The balanced data is saved back to the file.
3. **Defining Variables:**
* `project_dir:` Sets the project directory path.
* `raw_data:` Specifies the path for the raw merged data file.
* `output:` Specifies the path for the cleaned and processed data file.
* `input_folder:` Determines the directory where the input CSV files are stored.
4. **Main Execution Block:**
* The script includes a main block that calls the defined functions in sequence to process the data:
* **merge_csv_files:** Merges all brand-specific CSV files into a single raw data file.
* **remove_invalid_horse_power:** Removes rows with invalid horsepower values from the raw data.
* **remove_units:** Strips unit labels from numeric columns and formats them.
* **convert_to_float:** Converts relevant columns to float data type and filters out invalid rows.
* **remove_brands_below_treshold:** Removes brands with fewer than the specified number of listings.
* **balance_data:** Balances the dataset by oversampling brands with fewer listings.

### Key Feature
* **Separate CSV Files for Each Brand:** The script processes the raw data collected from separate CSV files for each car brand, ensuring that each brand's data is merged, cleaned, and balanced individually before being combined into a comprehensive dataset. This organization facilitates easier data management and analysis.

# RandomForest_Training.py Overview
The `RandomForest_Training.py` script is designed to train a Random Forest machine learning model using the preprocessed vehicle data. The script performs several steps to load the data, preprocess it, train the model, and evaluate its performance. The trained model is then saved for future use. Below is a detailed breakdown of the script's functionality:

1. **Importing Libraries:**
 - The script starts by importing necessary libraries such as `os`, `pandas`, `sklearn`, and `joblib`.
 - `pandas` is used for data manipulation, `sklearn` for machine learning tasks, and `joblib` for saving the trained model.

2. **Defining Variables:**
- `project_dir`: Sets the project directory path.
- `data`: Specifies the path to the preprocessed dataset file (`output.csv`).
- `model_file`: Specifies the path where the trained Random Forest model will be saved (`random_forest_model.pkl`).

3. **Loading and Preprocessing Data:**

- The dataset is loaded from the specified CSV file into a DataFrame.
- The `price_eur_formatted` column is converted to a float data type after removing commas.
- Categorical features (`brand_name`, `car_model`, `gearbox`, `fuel`) are one-hot encoded using `pd.get_dummies()`, converting them into numerical format suitable for machine learning models.

4. **Defining Features and Labels:**
- X is defined as the DataFrame excluding the `price_eur_formatted` column (features).
- y is defined as the `price_eur_formatted` column (labels).

5. **Splitting Data:**
- The dataset is split into training and testing sets using `train_test_split()` with an 80-20 split and a random state of 42 for reproducibility.

6. **Training the Random Forest Model:**
- A `RandomForestRegressor` model is initialized with 100 estimators and a random state of 42.
- The training data is split into batches to handle large datasets efficiently. The batch size is set to 10,000, and the number of batches is calculated.
- The model is trained incrementally on each batch using a loop that fits the model to each subset of the training data.

7. **Evaluating the Model:**
- After training, the model's performance is evaluated on the test set.
- Predictions are made using `model.predict(X_test)`.
- The mean squared error (MSE) between the predicted and actual values is calculated and printed. The MSE provides a measure of the model's prediction accuracy.

8. **Saving the Model:**
- The trained model is saved to a file using `joblib.dump()`, allowing it to be loaded and used later without retraining.

### Key Feature
- **R² Score of 0.77:** The model achieves an R² score of approximately 0.77 on the dataset, indicating that 77% of the variance in the vehicle prices can be explained by the features used in the model. This reflects a relatively high level of predictive accuracy.
## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.




