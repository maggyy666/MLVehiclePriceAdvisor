import pandas as pd
import joblib

# Wczytaj zapisany model
model = joblib.load('random_forest_model.pkl')

# Wczytaj dane z pliku CSV
data = pd.read_csv('cleaned_mileage_data.csv')
data['price_eur_formatted'] = data['price_eur_formatted'].str.replace(',', '').astype(float)

# Kodowanie zmiennych kategorycznych za pomocą get_dummies
data_encoded = pd.get_dummies(data, columns=['brand_name', 'car_model', 'gearbox', 'fuel'])


# Funkcja do przewidywania ceny na podstawie marki i modelu pojazdu
def predict_price(brand_name, car_model):
    # Sprawdź, czy marka i model pojazdu znajdują się w danych
    if (data_encoded['brand_name_' + brand_name] == 1).any() & (data_encoded['car_model_' + car_model] == 1).any():
        # Znajdź indeks rekordu dla podanej marki i modelu
        idx = (data_encoded['brand_name_' + brand_name] == 1) & (data_encoded['car_model_' + car_model] == 1)
        # Przewidź cenę dla danego indeksu
        predicted_price = model.predict(data_encoded[idx].drop(['price_eur_formatted'], axis=1))
        return predicted_price[0]
    else:
        return "Nie znaleziono informacji dla podanej marki i modelu."


# Funkcja do wyświetlania wszystkich modeli danej marki
def display_models_by_brand(brand_name):
    models = data.loc[data['brand_name'] == brand_name, 'car_model'].unique()
    print("Modele marki", brand_name + ":")
    for i, model in enumerate(models, 1):
        if i % 5 == 0:
            print(model)
        else:
            print(model, end=", ")
    print()


# Przykład użycia programu
if __name__ == "__main__":
    brand_name = input("Podaj markę pojazdu: ")
    car_model = input("Podaj model pojazdu: ")
    predicted_price = predict_price(brand_name, car_model)
    if isinstance(predicted_price, str):
        print(predicted_price)
    else:
        print(f"Optymalna cena dla {brand_name} {car_model}: {predicted_price} EUR")

    # Wyświetl wszystkie modele danej marki
    display_models_by_brand(brand_name)
