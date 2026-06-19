import logging
import math
import polars as pl

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

RAW_PATH = "data/raw/nyc_taxi_trips.csv"
OUTPUT_PATH = "data/processed/cleaned_taxi_trips.parquet"

NYC_LON_MIN, NYC_LON_MAX = -74.05, -73.70
NYC_LAT_MIN, NYC_LAT_MAX = 40.55, 40.92


def haversine_km(lon1, lat1, lon2, lat2):
    """Returns the great-circle distance in km between two coordinates."""
    R = 6371  # Earth's radius in km
    lon1_r, lat1_r, lon2_r, lat2_r = [
        c * math.pi / 180 for c in (lon1, lat1, lon2, lat2)
    ]
    dlon = lon2_r - lon1_r
    dlat = lat2_r - lat1_r
    a = (dlat / 2).sin() ** 2 + lat1_r.cos() * lat2_r.cos() * (dlon / 2).sin() ** 2
    return 2 * R * a.sqrt().arcsin()


def main():
    logger.info("Reading raw CSV from %s", RAW_PATH)
    df = pl.read_csv(RAW_PATH)
    start_count = df.height
    logger.info("Loaded %d rows", start_count)

    df = df.with_columns(
        pl.col("pickup_datetime").str.to_datetime("%Y-%m-%d %H:%M:%S"),
        pl.col("dropoff_datetime").str.to_datetime("%Y-%m-%d %H:%M:%S"),
    )

    df = df.with_columns(
        (pl.col("store_and_fwd_flag") == "Y").alias("store_and_fwd_flag")
    )

    df = df.filter(pl.col("trip_duration").is_between(30, 14400))
    logger.info("After duration filter: %d rows (dropped %d)", df.height, start_count - df.height)

    before = df.height
    df = df.filter(pl.col("passenger_count").is_between(1, 6))
    logger.info("After passenger filter: %d rows (dropped %d)", df.height, before - df.height)

    before = df.height
    df = df.filter(
        pl.col("pickup_longitude").is_between(NYC_LON_MIN, NYC_LON_MAX)
        & pl.col("pickup_latitude").is_between(NYC_LAT_MIN, NYC_LAT_MAX)
        & pl.col("dropoff_longitude").is_between(NYC_LON_MIN, NYC_LON_MAX)
        & pl.col("dropoff_latitude").is_between(NYC_LAT_MIN, NYC_LAT_MAX)
    )
    logger.info("After coordinate filter: %d rows (dropped %d)", df.height, before - df.height)

    df = df.with_columns(
        (pl.col("trip_duration") / 60).alias("trip_duration_minutes"),
        pl.col("pickup_datetime").dt.hour().alias("pickup_hour"),
        pl.col("pickup_datetime").dt.weekday().alias("pickup_day_of_week"),
        haversine_km(
            pl.col("pickup_longitude"), pl.col("pickup_latitude"),
            pl.col("dropoff_longitude"), pl.col("dropoff_latitude"),
        ).alias("trip_distance_km"),
    )

    assert df.height > 0, "No rows left after cleaning — something is wrong!"
    assert df.null_count().sum_horizontal().sum() == 0, "Unexpected nulls found after cleaning!"

    logger.info("Final cleaned row count: %d", df.height)
    logger.info("Writing Parquet to %s", OUTPUT_PATH)
    df.write_parquet(OUTPUT_PATH)
    logger.info("Done.")


if __name__ == "__main__":
    main()