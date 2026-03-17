from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from datetime import datetime
from map_loading_helper import (
    load_new_price_files,
    append_price_monitoring,
    append_violations_table,
    generate_letters
)

def run_price_monitoring():
    batch_id = datetime.now().strftime("%Y%m%d%H%M%S")
    append_price_monitoring(batch_id)

with DAG(
    dag_id="map_compliance_pipeline",
    start_date=datetime(2026,3,16),
    schedule="@daily",
    catchup=False
) as dag:

    load_files = PythonOperator(
        task_id="load_new_seller_files",
        python_callable=load_new_price_files
    )

    monitor_prices = PythonOperator(
        task_id="price_monitoring",
        python_callable=run_price_monitoring
    )

    violations = PythonOperator(
        task_id="update_violation_table",
        python_callable=append_violations_table
    )

    letters = PythonOperator(
        task_id="generate_violation_letters",
        python_callable=generate_letters
    )

    load_files >> monitor_prices >> violations >> letters