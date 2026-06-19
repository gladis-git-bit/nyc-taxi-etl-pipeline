import polars as pl

df = pl.read_parquet("data/processed/cleaned_taxi_trips.parquet")
print("Shape:", df.shape)
print(df.head())
print()
print("New columns check:")
print(df.select(["trip_duration_minutes", "pickup_hour", "pickup_day_of_week", "trip_distance_km"]).head())