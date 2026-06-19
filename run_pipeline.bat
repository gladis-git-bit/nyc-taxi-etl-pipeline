@echo off
cd /d C:\Users\aakas\Downloads\nyc-taxi-etl-pipeline
call venv\Scripts\activate.bat
python run_pipeline.py >> pipeline_log.txt 2>&1