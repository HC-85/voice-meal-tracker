from dagster import DailyPartitionsDefinition

START_DATE = "2025-06-01"
daily_partitions = DailyPartitionsDefinition(start_date=START_DATE)
