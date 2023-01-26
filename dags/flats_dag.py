import os
import json
import pandas as pd

from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator

from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from sqlalchemy import create_engine

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

    def get_data_from_file(**kwargs):
        data = []
        with open("data/flats.jsonl", "r") as file:
            for line in file:
                data.append(json.loads(line))
        df = pd.DataFrame(data=data)
        dict_df = df.to_dict("records")
        ti = kwargs["ti"]
        ti.xcom_push("dict_df", dict_df)

    def take_df(ti):
        df = pd.DataFrame.from_records(
            data=ti.xcom_pull(task_ids="get_data_for_df", key="dict_df")
        )
        
        engine = create_engine('postgresql://admin:admin@0.0.0.0:5432/admin')
        df.to_sql('flats', engine)

    t1 = PythonOperator(task_id="scrape_flats_data", python_callable=process_spider)

    t2 = PythonOperator(task_id="get_data_for_df", python_callable=get_data_from_file)

    t3 = PythonOperator(task_id="print_df", python_callable=take_df)

    t1 >> t2 >> t3
