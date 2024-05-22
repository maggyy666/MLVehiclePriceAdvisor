import os.path

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import joblib
import os

project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

data = os.path.join(project_dir, 'dataset_files', 'output.csv')
model_file = os.path.join(project_dir, 'random_forest_model.pkl')

data['price_eur_formatted'] = data['price_eur_formatted'].str.replace(',', '').astype(float)

data_encoded = pd.get_dummies(data, columns=['brand_name', 'car_model', 'gearbox', 'fuel'])

X = data_encoded.drop(['price_eur_formatted'], axis=1)  # Usuń kolumnę z cenami, to będzie nasza etykieta
y = data_encoded['price_eur_formatted']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

batch_size = 10000
num_batches = len(X_train) // batch_size + 1

model = RandomForestRegressor(n_estimators=100, random_state=42)

for i in range(num_batches):
    start_idx = i * batch_size
    end_idx = min((i + 1) * batch_size, len(X_train))
    X_batch = X_train.iloc[start_idx:end_idx]
    y_batch = y_train.iloc[start_idx:end_idx]
    model.fit(X_batch, y_batch)


y_pred = model.predict(X_test)
joblib.dump(model, model_file)
mse = mean_squared_error(y_test, y_pred)
print("Mean Squared Error:", mse)
