import os
import json
import pandas as pd

from airflow import DAG
from sqlalchemy import create_engine
from airflow.models import Variable
from airflow.hooks.base import BaseHook
from datetime import datetime, timedelta
from airflow.operators.python import PythonOperator
from functions.flats_dag_functions import FlatsFunctions



DATA_PATH = Variable.get("DATA_PATH")
POSTGRES_USER_DATA = Variable.get("POSTGRES_USER_DATA")
POSTGRES_PASSWORD_DATA = Variable.get("POSTGRES_PASSWORD_DATA")
POSTGRES_DB_DATA = Variable.get("POSTGRES_DB_DATA")
connection = BaseHook.get_connection("Postgres_conn")

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

    def get_data_from_file(**kwargs):
        data = []
        with open(f"{DATA_PATH}/flats.jsonl", "r") as file:
            for line in file:
                data.append(json.loads(line))
        df = pd.DataFrame(data=data)
        dict_df = df.to_dict("records")
        ti = kwargs["ti"]
        ti.xcom_push("dict_df", dict_df)

    def save_df_to_postgres(ti):
        df = pd.DataFrame.from_records(
            data=ti.xcom_pull(task_ids="get_data_for_df", key="dict_df")
        )
        connection_string = 'postgresql+psycopg2://' + str(connection.login) + ':' + str(connection.password) + '@' + str(connection.host) + ':' + str(connection.port) + '/' + str(connection.schema)
        # engine = create_engine(
        #     f"postgresql+psycopg2://{POSTGRES_USER_DATA}:{POSTGRES_PASSWORD_DATA}@localhost:5432/{POSTGRES_DB_DATA}"
        # )
        engine = create_engine(connection_string)
        df.to_sql("flats", engine)

    scrape_flats_data = PythonOperator(
        task_id="scrape_flats_data", python_callable=FlatsFunctions.process_spider
    )

    get_data_for_df = PythonOperator(
        task_id="get_data_for_df", python_callable=get_data_from_file
    )

    save_data_to_postgres = PythonOperator(
        task_id="save_data_to_postgres", python_callable=save_df_to_postgres
    )

    scrape_flats_data >> get_data_for_df >> save_data_to_postgres
