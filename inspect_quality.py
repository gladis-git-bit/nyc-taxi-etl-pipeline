import polars as pl

df = pl.read_csv("data/raw/nyc_taxi_trips.csv")

print("Passenger count distribution:")
print(df.group_by("passenger_count").len().sort("passenger_count"))
print()

print("Trips under 30 seconds:", df.filter(pl.col("trip_duration") < 30).height)
print("Trips over 4 hours (14400 sec):", df.filter(pl.col("trip_duration") > 14400).height)
print()

nyc_box = (
    (pl.col("pickup_longitude").is_between(-74.05, -73.70)) &
    (pl.col("pickup_latitude").is_between(40.55, 40.92)) &
    (pl.col("dropoff_longitude").is_between(-74.05, -73.70)) &
    (pl.col("dropoff_latitude").is_between(40.55, 40.92))
)
print("Trips with coordinates outside NYC box:", df.filter(~nyc_box).height)
print("Trips with coordinates inside NYC box:", df.filter(nyc_box).height)