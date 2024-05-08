import pandas as pd
def clean_data(csv_file):
    df = pd.read_csv(csv_file, header=None)
    df.columns = ['data_id', 'car_id', 'brand_name', 'car_model', 'mileage',
                  'price_pln_formatted', 'price_eur_formatted', 'engine_power',
                  'gearbox', 'year', 'fuel', 'horse_power', 'current_page']
    df = df.drop(['data_id','car_id','current_page'], axis=1)
    df['mileage'] = df['mileage'].str.replace(' km', '')
    df['horse_power'] = df['horse_power'].str.replace(' KM', '')
    df['engine_power'] = df['engine_power'].str.replace(' cm3', '')
    df = df.dropna()
    df = df[df['horse_power'].str.match('^\d+$')]
    df.to_csv('cleaned_data.csv', index = False)
    print("Success")
clean_data('raw_data.csv')
