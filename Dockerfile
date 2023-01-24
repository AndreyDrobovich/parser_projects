FROM apache/airflow:2.5.1-python3.10
COPY requirements.txt /tmp/
RUN python -m pip install --upgrade pip
RUN pip install --requirement /tmp/requirements.txt