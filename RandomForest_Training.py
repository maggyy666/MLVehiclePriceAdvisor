import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestRegressor
from joblib import dump


data = pd.read_csv("cleaned_mileage_data.csv")

# Fill missing values in the 'mileage' column with zero
data['mileage'].fillna('0', inplace=True)

# Wykonywanie kodowania kategorycznego na kolumnach "brand_name" i "car_model"
data = pd.get_dummies(data, columns=['brand_name', 'car_model'])

# Konwersja kolumn "mileage" i "price_pln_formatted" na float
data['mileage'] = data['mileage'].astype(str).str.replace(',', '').astype(float)
data['price_pln_formatted'] = data['price_pln_formatted'].str.replace(',', '').astype(float)

# Usunięcie niepotrzebnych kolumn
data.drop(columns=['price_eur_formatted'], inplace=True)

X = data.drop(columns=['price_pln_formatted'])
y = data['price_pln_formatted']

model = RandomForestRegressor(n_estimators=100, random_state=42)
scores = cross_val_score(model, X, y, cv=5, n_jobs=-1)

print("Cross-Validation scores:", scores)
print("Mean R^2:", scores.mean())

dump(model, 'random_forest_model.pkl')
