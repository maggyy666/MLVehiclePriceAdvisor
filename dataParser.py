import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
from joblib import load
import os


def preprocess_input(input_data, X):
    # Przetwarzanie danych wejściowych użytkownika tak, aby pasowały do formatu oczekiwanego przez model

    # Sprawdzenie, czy podany model samochodu istnieje w zestawie danych
    car_model_cols = [col for col in X.columns if 'car_model' in col and input_data['car_model'].lower() in col.lower()]
    if not car_model_cols:
        raise ValueError("The provided car model '{}' does not exist in the dataset.".format(input_data['car_model']))

    # Użycie pierwszego znalezionego dopasowania
    car_model_index = X.columns.get_loc(car_model_cols[0])

    # Pozostałe indeksy cech
    brand_name_index = X.columns.get_loc('brand_name_' + input_data['brand_name'])
    mileage_index = X.columns.get_loc('mileage')
    year_index = X.columns.get_loc('year')
    gearbox_index = X.columns.get_loc('gearbox_' + input_data['gearbox'])
    fuel_index = X.columns.get_loc('fuel_' + input_data['fuel'])

    processed_input_data = [
        brand_name_index, car_model_index, input_data['mileage'], input_data['year'], gearbox_index, fuel_index
    ]

    return processed_input_data


def predict_car_price(input_data, model, X):
    # Przewidywanie ceny samochodu na podstawie danych wejściowych
    input_data = preprocess_input(input_data, X)
    predicted_price = model.predict([input_data])
    return predicted_price[0]


def get_user_input():
    brand_name = input("Podaj markę samochodu: ")
    car_model = input("Podaj model samochodu: ")
    mileage = float(input("Podaj przebieg samochodu (w km): "))
    year = int(input("Podaj rok produkcji samochodu: "))
    gearbox = input("Podaj typ skrzyni biegów (Manualna/Automatyczna): ")
    fuel = input("Podaj rodzaj paliwa (Benzyna/Diesel): ")

    # Tutaj możesz dodać kod do pobrania innych danych wejściowych od użytkownika, takich jak pojemność silnika, liczba koni mechanicznych itp.

    # Zwrócenie danych wejściowych w formie słownika
    input_data = {
        'brand_name': brand_name,
        'car_model': car_model,
        'mileage': mileage,
        'year': year,
        'gearbox': gearbox,
        'fuel': fuel
        # Dodaj pozostałe dane wejściowe
    }

    return input_data


def main():
    # Wczytanie wytrenowanego modelu
    model = load('random_forest_model.pkl')

    # Wczytanie przetworzonych danych
    X = pd.read_csv('cleaned_mileage_data.csv')

    # Pobranie danych wejściowych od użytkownika
    input_data = get_user_input()

    # Przewidywanie ceny samochodu na podstawie danych wejściowych
    predicted_price = predict_car_price(input_data, model, X)

    # Wyświetlenie przewidywanej ceny samochodu
    print("Przewidywana cena samochodu: ", predicted_price)


if __name__ == "__main__":
    main()
