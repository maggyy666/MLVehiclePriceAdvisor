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

def predict_price(brand_name, car_model):
    if (data_encoded['brand_name_' + brand_name] == 1).any() & (data_encoded['car_model_' + car_model] == 1).any():
        idx = (data_encoded['brand_name_' + brand_name] == 1) & (data_encoded['car_model_' + car_model] == 1)
        predicted_price = model.predict(data_encoded[idx].drop(['price_eur_formatted'], axis=1))
        return predicted_price[0]
    else:
        return "Nie znaleziono informacji dla podanej marki i modelu."

def display_models_by_brand(brand_name):
    models = data.loc[data['brand_name'] == brand_name, 'car_model'].unique()
    print("Modele marki", brand_name + ":")
    for i, model in enumerate(models, 1):
        if i % 5 == 0:
            print(model)
        else:
            print(model, end=", ")
    print()

if __name__ == "__main__":
    brand_name = input("Podaj markę pojazdu: ")
    display_models_by_brand(brand_name)
    car_model = input("Podaj model pojazdu: ")
    predicted_price = predict_price(brand_name, car_model)
    if isinstance(predicted_price, str):
        print(predicted_price)
    else:
        print(f"Optymalna cena dla {brand_name} {car_model}: {predicted_price} EUR")
