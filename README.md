
# NYC Taxi ETL Pipeline

An end-to-end data engineering pipeline that extracts NYC taxi trip data, cleans and transforms it with Polars, converts it to Parquet, and loads it into Google BigQuery — fully orchestrated and scheduled to run automatically.

## Architecture

**Architecture Diagram:** [docs/architecture.svg](docs/architecture.svg)

## What it does

- **Extract** — Reads approximately 1.45 million raw NYC taxi trip records from a Kaggle CSV dataset.
- **Transform** — Uses Polars to:
  - Parse and type datetime columns.
  - Filter out unrealistic trip durations (less than 30 seconds or greater than 4 hours).
  - Filter out invalid passenger counts and GPS coordinates outside NYC.
  - Engineer new features such as trip distance (using the haversine formula), pickup hour, and day of week.
- **Convert** — Writes the cleaned dataset to a compressed Parquet file.
- **Load** — Pushes the Parquet file into Google BigQuery using an idempotent full-refresh load, making it safe to rerun without creating duplicates.
- **Orchestrate and Schedule** — `run_pipeline.py` executes all steps in one command, and Windows Task Scheduler runs it automatically every day.

## Results

- Cleaned 1,447,081 valid trips from 1,458,644 raw records (approximately 0.8% removed as bad data).
- Complete pipeline execution time is under 40 seconds.
- Average trip distance and trip volume vary by hour of the day, showing realistic ride patterns in the cleaned dataset.

## Tech Stack

- Python 3.12
- Polars for fast dataframe transformations
- PyArrow for Parquet read and write operations
- Google BigQuery as the cloud data warehouse
- python-dotenv for secure local configuration management
- Windows Task Scheduler for automation

## Project Structure
```
ynyc-taxi-etl-pipeline/
│
├── data/
│   ├── raw/                  # Original CSV (not tracked in Git)
│   └── processed/            # Cleaned Parquet output (not tracked in Git)
│
├── docs/
│   └── architecture.svg
│
├── inspect_data.py           # Initial data profiling
├── inspect_quality.py        # Data quality investigation
├── transform.py              # Extract, clean, and feature engineering
├── load.py                   # Idempotent load into BigQuery
├── run_pipeline.py           # Orchestrates the full pipeline
├── run_pipeline.bat          # Entry point for Task Scheduler
├── requirements.txt
└── .env                      # Local config (not tracked in Git)
```



# How to Run It

## 1. Clone the repository and create a virtual environment.

### Create a virtual environment:
```bash
python -m venv venv
```

### Activate the virtual environment:
```bash
venv\Scripts\activate
```

### Install dependencies:
```bash
pip install -r requirements.txt
```

## 2. Download the dataset "NYC Taxi Trip Duration" from Kaggle and place the CSV file at:
`data/raw/nyc_taxi_trips.csv`

## 3. Create a `.env` file with the following variables:
```plaintext
GCP_PROJECT_ID=your-project-id
BQ_DATASET_ID=your-dataset-id
BQ_TABLE_ID=your-table-id
```

## 4. Authenticate with Google Cloud:
```bash
gcloud auth application-default login
```

## 5. Run the complete pipeline:
```bash
python run_pipeline.py
```