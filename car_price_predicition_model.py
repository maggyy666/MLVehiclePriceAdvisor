import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LinearRegression

data = pd.read_csv("cleaned_data.csv")

data = pd.get_dummies(data, columns=['brand_name'])

label_encoder = LabelEncoder()
data['car_model'] = label_encoder.fit_transform(data['car_model'])
data['gearbox'] = label_encoder.fit_transform(data['gearbox'])
data['fuel'] = label_encoder.fit_transform(data['fuel'])
data['mileage'] = data['mileage'].str.replace(' ','')
data['engine_power'] = data['engine_power'].str.replace(' ','')

# Upewnijmy się, że kolumny są typu str przed użyciem .str.replace()
str_columns = ['mileage', 'price_pln_formatted', 'price_eur_formatted']
for col in str_columns:
    if data[col].dtype == 'object':
        data[col] = data[col].str.replace(',', '').astype(float)

data['engine_power'] = data['engine_power'].astype(float)
data['year'] = data['year'].astype(int)
data['horse_power'] = data['horse_power'].astype(int)

X = data.drop(columns=['price_pln_formatted', 'price_eur_formatted'])
y = data['price_pln_formatted']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Przykładowy model regresji liniowej
model = LinearRegression()
model.fit(X_train, y_train)

# Oceniamy model
train_score = model.score(X_train, y_train)
test_score = model.score(X_test, y_test)

print("Train R^2:", train_score)
print("Test R^2:", test_score)
