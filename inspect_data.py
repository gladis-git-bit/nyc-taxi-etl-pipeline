import polars as pl

df = pl.read_csv("data/raw/nyc_taxi_trips.csv")

print("Shape:", df.shape)
print()
print("Schema:")
print(df.schema)
print()
print("First 5 rows:")
print(df.head())
print()
print("Null counts per column:")
print(df.null_count())
print()
print("Summary stats:")
print(df.describe())