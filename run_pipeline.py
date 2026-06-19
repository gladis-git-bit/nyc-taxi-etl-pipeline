import logging
import time

import transform
import load

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def main():
    start_time = time.time()
    logger.info("=== Starting NYC Taxi ETL Pipeline ===")

    logger.info("--- Step 1/2: Transform (clean CSV, write Parquet) ---")
    transform.main()

    logger.info("--- Step 2/2: Load (push Parquet to BigQuery) ---")
    load.main()

    elapsed = time.time() - start_time
    logger.info("=== Pipeline finished successfully in %.2f seconds ===", elapsed)


if __name__ == "__main__":
    main()