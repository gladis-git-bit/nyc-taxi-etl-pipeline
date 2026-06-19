import logging
import os

from dotenv import load_dotenv
from google.cloud import bigquery

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

PARQUET_PATH = "data/processed/cleaned_taxi_trips.parquet"


def main():
    load_dotenv()  # reads variables from your .env file

    project_id = os.getenv("GCP_PROJECT_ID")
    dataset_id = os.getenv("BQ_DATASET_ID")
    table_id = os.getenv("BQ_TABLE_ID")

    if not all([project_id, dataset_id, table_id]):
        raise ValueError("Missing config — check your .env file has all three variables set.")

    table_ref = f"{project_id}.{dataset_id}.{table_id}"
    logger.info("Target table: %s", table_ref)

    client = bigquery.Client(project=project_id)

    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.PARQUET,
        write_disposition="WRITE_TRUNCATE",  # full refresh = idempotent, no duplicate runs
    )

    logger.info("Reading Parquet file from %s", PARQUET_PATH)
    with open(PARQUET_PATH, "rb") as source_file:
        load_job = client.load_table_from_file(source_file, table_ref, job_config=job_config)

    logger.info("Load job started, waiting for it to finish...")
    load_job.result()  # blocks until the job is done

    table = client.get_table(table_ref)
    logger.info("Success. Table now has %d rows and %d columns.", table.num_rows, len(table.schema))


if __name__ == "__main__":
    main()