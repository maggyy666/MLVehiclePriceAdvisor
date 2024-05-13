import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
from joblib import load
import os


def preprocess_input(input_data, X, selected_brand):
    print("Input data before preprocessing:", input_data)

    # Filtrowanie danych tylko dla wybranej marki pojazdu
    X_filtered = X[X['brand_name'] == selected_brand]

    # Sprawdzenie, czy podany model samochodu jest zawarty w nazwach modeli wybranej marki
    car_columns = [col for col in X_filtered.columns if 'model' in col.lower()]
    if not car_columns:
        raise ValueError("No car model column found for the selected brand.")
    car_models = set(X_filtered[car_columns[0]])

    for model in car_models:
        if model in input_data['car_model']:
            car_model = model
            break
    else:
        raise ValueError("The provided car model '{}' does not exist for the selected brand.".format(input_data['car_model']))

    # Znalezienie indeksu kolumny odpowiadającej nazwie modelu
    car_model_index = X_filtered.columns.get_loc(car_columns[0])

    # Znalezienie indeksu kolumny odpowiadającej marce samochodu
    brand_name_index = X_filtered.columns.get_loc('brand_name')

    # Pozostałe indeksy cech
    mileage_index = X_filtered.columns.get_loc('mileage')
    year_index = X_filtered.columns.get_loc('year')
    gearbox_index = X_filtered.columns.get_loc('gearbox')
    fuel_index = X_filtered.columns.get_loc('fuel')

    processed_input_data = [
        brand_name_index, car_model_index, input_data['mileage'], input_data['year'], gearbox_index, fuel_index
    ]

    print("Input data after preprocessing:", processed_input_data)

    return processed_input_data



def predict_car_price(input_data, model, X):
    # Wybór marki pojazdu
    selected_brand = input_data['brand_name']

    # Filtrowanie danych tylko dla wybranej marki pojazdu
    X_filtered = X[X['brand_name'] == selected_brand]

    # Przetwarzanie danych wejściowych
    input_data_processed = preprocess_input(input_data, X_filtered, selected_brand)
    print("Processed input data:", input_data_processed)

    # Wydrukujmy również dane wejściowe dla modelu
    print("Input data for model:", X_filtered.iloc[0])  # Wydrukuj dane pierwszego samochodu Ferrari w zbiorze danych

    # Tworzenie danych wejściowych w formacie zgodnym z modelem
    num_features_expected = 68  # Oczekiwana liczba cech przez model
    input_data_for_model = [0] * num_features_expected
    input_data_indices = [0, 1, 2, 3, 4, 5]  # Indeksy cech w przetworzonych danych

    # Wypełnienie wartości cech na odpowiednich indeksach
    for idx, val in zip(input_data_indices, input_data_processed):
        input_data_for_model[idx] = val

    predicted_price = model.predict([input_data_for_model])
    return predicted_price[0]



def get_user_input():
    brand_name = input("Podaj markę samochodu: ")

    # Wczytanie danych w celu znalezienia wszystkich modeli dla podanej marki
    data = pd.read_csv("cleaned_mileage_data.csv")
    available_models = data[data['brand_name'] == brand_name]['car_model'].unique()

    print("Available car models:")
    for model in available_models:
        print(model)

    car_model = input("Podaj model samochodu: ")
    mileage = float(input("Podaj przebieg samochodu (w km): "))
    year = int(input("Podaj rok produkcji samochodu: "))
    gearbox = input("Podaj typ skrzyni biegów (Manualna/Automatyczna): ")
    fuel = input("Podaj rodzaj paliwa (Benzyna/Diesel): ")

    # Zwrócenie danych wejściowych w formie słownika
    input_data = {
        'brand_name': brand_name,
        'car_model': car_model,
        'mileage': mileage,
        'year': year,
        'gearbox': gearbox,
        'fuel': fuel
    }

    return input_data


def fit_model(X, y):
    # Inicjalizacja modelu RandomForestRegressor
    model = RandomForestRegressor(n_estimators=100, random_state=42)

    # Dopasowanie modelu do danych treningowych
    model.fit(X, y)

    return model


def main():
    # Wczytanie przetworzonych danych
    X = pd.read_csv('cleaned_mileage_data.csv')

    # Podział na zbiór cech (X) i etykiety (y)
    y = X['price_pln_formatted']
    X = X.drop(columns=['price_pln_formatted', 'price_eur_formatted', 'brand_name'])

    # Dopasowanie modelu do danych treningowych
    model = fit_model(X, y)
    print("Model fitted successfully.")

    # Pobranie danych wejściowych od użytkownika
    input_data = get_user_input()

    # Przewidywanie ceny samochodu na podstawie danych wejściowych
    predicted_price = predict_car_price(input_data, model, X)

    # Wyświetlenie przewidywanej ceny samochodu
    print("Input data:", input_data)
    print("Przewidywana cena samochodu:", predicted_price)


if __name__ == "__main__":
    main()
