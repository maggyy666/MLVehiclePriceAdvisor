import pandas as pd
import joblib
import os

project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
model_path = os.path.join(project_dir, 'random_forest_model.pkl')
data_path = os.path.join(project_dir, 'dataset_files', 'output.csv')

model = joblib.load(model_path)
data = pd.read_csv(data_path)

data['price_eur_formatted'] = data['price_eur_formatted'].str.replace(',', '').astype(float)
data_encoded = pd.get_dummies(data, columns=['brand_name', 'car_model', 'gearbox', 'fuel'])


def predict_price(brand_name, car_model, mileage, production_year):
    brand_col = f'brand_name_{brand_name}'
    model_col = f'car_model_{car_model}'

    if brand_col in data_encoded.columns and model_col in data_encoded.columns:
        model_data = data_encoded[(data_encoded[brand_col] == 1) & (data_encoded[model_col] == 1)]

        if not model_data.empty:
            avg_mileage = model_data['mileage'].mean()
            avg_year = model_data['year'].mean()
            idx = (data_encoded[brand_col] == 1) & (data_encoded[model_col] == 1)

            predicted_price = model.predict(data_encoded[idx].drop(['price_eur_formatted'], axis=1))
            predicted_price = predicted_price[0]


            while mileage > avg_mileage:
                predicted_price *= 0.995
                mileage -= 10000
            while mileage < avg_mileage:
                predicted_price *= 1.005
                mileage += 10000

            while production_year < avg_year:
                predicted_price *= 0.95
                production_year += 1
            while production_year > avg_year:
                predicted_price *= 1.05
                production_year -= 1

            return max(predicted_price, 0)
        else:
            return "No information found for the specified make and model."
    else:
        return "No information found for the specified make and model."


def display_models_by_brand(brand_name):
    models = data.loc[data['brand_name'] == brand_name, 'car_model'].unique()
    print("Brand models", brand_name + ":")
    for i, model in enumerate(models, 1):
        if i % 5 == 0:
            print(model)
        else:
            print(model, end=", ")
    print()


if __name__ == "__main__":
    brand_name = input("Enter car brand: ")
    display_models_by_brand(brand_name)
    car_model = input("Enter car model: ")
    mileage = float(input("Enter mileage (in km): "))
    production_year = int(input("Enter production year: "))

    predicted_price = predict_price(brand_name, car_model, mileage, production_year)
    if isinstance(predicted_price, str):
        print(predicted_price)
    else:
        print(
            f"Optimal price for: {brand_name} {car_model} with {mileage} km and year {production_year}: {predicted_price} EUR / {predicted_price * 4.25} PLN")
