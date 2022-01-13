import pandas as pd

rating_training_file = 'BX-CSV-Dump/BX-Book-Ratings.csv'

df = pd.read_csv(rating_training_file, encoding='ISO-8859–1', sep=';', on_bad_lines='skip')

print(df.head())
print(df.values.size)