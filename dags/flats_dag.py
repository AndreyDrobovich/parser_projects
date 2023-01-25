import os
import json
import pandas as pd

from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator

from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from services.scrapy_code.spiders.onliner_spider import FlatsSpider
from services.scrapy_code import settings as my_settings


with DAG(
    dag_id="flat_dag",
    default_args={
        "depends_on_past": False,
        "email": ["airflow@example.com"],
        "email_on_failure": False,
        "email_on_retry": False,
        "retries": 1,
        "retry_delay": timedelta(minutes=5),
    },
    start_date=datetime.now(),
    catchup=False,
) as dag:

    def process_spider():
        crawler_settings = Settings()
        crawler_settings.setmodule(my_settings)
        process = CrawlerProcess(settings=crawler_settings)
        process.crawl(FlatsSpider)
        process.start()

    def save_data_to_db():
        data = []
        with open("data/flats.jsonl", "r") as file:
            for line in file:
                data.append(json.loads(line))
        df = pd.DataFrame(data=data)
        print(df.columns)

    t1 = PythonOperator(task_id="scrape_flats_data", python_callable=process_spider)

    t2 = PythonOperator(task_id="show_date", python_callable=save_data_to_db)

    t1 >> t2
