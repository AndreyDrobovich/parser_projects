from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from services.scrapy_code.spiders.onliner_spider import FlatsSpider


with DAG(
    dag_id="parser_dag",
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
        process = CrawlerProcess(get_project_settings())
        process.crawl(FlatsSpider)
        process.start()

    def print_date():
        return print(datetime.now())

    t1 = PythonOperator(task_id="scrape_data_from_site", python_callable=process_spider)

    t2 = PythonOperator(task_id="show_date", python_callable=print_date)

    t1 >> t2
