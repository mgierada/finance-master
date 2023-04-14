import pandas as pd

def read_data():
    df = pd.read_csv('data.csv', sep=';')
    return df
