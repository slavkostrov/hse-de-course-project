from datetime import datetime

from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
from modules.data.build_report import generate_fraud_report
from modules.data.dim_hist_load import load_to_dim_hist
from modules.data.dim_load import load_tables_to_dim
from modules.data.fact_load import load_fact_data
from modules.data.source import backup_data
from modules.data.staging_load import load_data_into_staging
from modules.db.utils import engine
from modules.models import create_tables

with DAG(
    "data_pipeline_dag",
    default_args={
        "owner": "airflow",
        "depends_on_past": False,
        "start_date": datetime(2024, 12, 19),  # noqa
        "retries": 1,
    },
    # TODO: тут надежней конкретное время указать
    schedule_interval="@daily",
    catchup=False,
) as dag:
    start_operator = EmptyOperator(task_id="start")
    create_tables_operator = PythonOperator(
        task_id="create_tables",
        python_callable=create_tables,
        op_kwargs={"engine": engine},
    )

    load_staging_operator = PythonOperator(
        task_id="load_staging",
        python_callable=load_data_into_staging,
        op_kwargs={"date": "{{ params.get('date', ds) }}", "engine": engine},
    )

    backup_data_operator = PythonOperator(
        task_id="backup_data",
        python_callable=backup_data,
        op_kwargs={"date": "{{ params.get('date', ds) }}"},
    )

    load_dim_operator = PythonOperator(
        task_id="load_dim",
        python_callable=load_tables_to_dim,
    )

    load_dim_hist_operator = PythonOperator(
        task_id="load_dim_hist",
        python_callable=load_to_dim_hist,
    )

    load_fact_operator = PythonOperator(
        task_id="load_fact",
        python_callable=load_fact_data,
    )

    generate_report_operator = PythonOperator(
        task_id="generate_report",
        python_callable=generate_fraud_report,
        op_kwargs={"date": "{{ params.get('date', ds) }}", "engine": engine},
    )

    end_operator = EmptyOperator(task_id="end")

    load_staging_operator >> backup_data_operator >> end_operator

    (
        start_operator
        >> create_tables_operator
        >> load_staging_operator
        >> load_dim_operator
        >> load_dim_hist_operator
        >> load_fact_operator
        >> generate_report_operator
        >> end_operator
    )
