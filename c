[1mdiff --git a/.gitignore b/.gitignore[m
[1mindex d5a4fee..9969ca1 100644[m
[1m--- a/.gitignore[m
[1m+++ b/.gitignore[m
[36m@@ -6,4 +6,5 @@[m
 processed_data/[m
 /dags/tasks/__pycache__[m
 models/*[m
[31m-!models/.gitkeep[m
\ No newline at end of file[m
[32m+[m[32m!models/.gitkeep[m
[32m+[m[32m/containers/rakuten-ml/__pycache__[m
\ No newline at end of file[m
[1mdiff --git a/dags/ml_pipeline_docker_dag.py b/dags/ml_pipeline_docker_dag.py[m
[1mindex c46d967..eb5fae4 100644[m
[1m--- a/dags/ml_pipeline_docker_dag.py[m
[1m+++ b/dags/ml_pipeline_docker_dag.py[m
[36m@@ -13,13 +13,14 @@[m [mwith DAG([m
     dag_id='ml_pipeline_docker',[m
     description='Machine Learning pipeline using Docker containers for Rakuten product classification',[m
     tags=['Rakuten', 'ML', 'MLOps', 'Docker'],[m
[31m-    schedule="*/5 * * * *",[m
[32m+[m[32m    schedule="*/15 * * * *",[m
     default_args={[m
         'owner': 'airflow',[m
         'start_date': datetime(2025, 6, 19),[m
         'retries': 1,[m
     },[m
     catchup=False,[m
[32m+[m[32m    max_active_runs=1,[m
     doc_md="""[m
     # ML Pipeline DAG (Docker Version)[m
     [m
[1mdiff --git a/dags/prepare_data_dag.py b/dags/prepare_data_dag.py[m
[1mindex 5d90088..8557498 100644[m
[1m--- a/dags/prepare_data_dag.py[m
[1m+++ b/dags/prepare_data_dag.py[m
[36m@@ -10,7 +10,7 @@[m [mwith DAG([m
     dag_id='prepare_data',[m
     description='Prepare data from raw_data directory',[m
     tags=['Rakuten'],[m
[31m-    schedule="*/5 * * * *",[m
[32m+[m[32m    schedule="*/15 * * * *",[m
     default_args={[m
         'owner': 'airflow',[m
         "start_date": datetime(2025, 6, 15),[m
[36m@@ -25,7 +25,7 @@[m [mwith DAG([m
         op_kwargs={[m
             'csv_path': "/opt/airflow/raw_data/x_train.csv",[m
             'table_name': "x_train",[m
[31m-            'num_rows': BATCH_SIZE[m
[32m+[m[32m            'end_row': BATCH_SIZE[m
         }[m
     )[m
     [m
[36m@@ -45,7 +45,7 @@[m [mwith DAG([m
         op_kwargs={[m
             'csv_path': "/opt/airflow/raw_data/y_train.csv",[m
             'table_name': "y_train",[m
[31m-            'num_rows': BATCH_SIZE[m
[32m+[m[32m            'end_row': BATCH_SIZE[m
         }[m
     )[m
     [m
[1mdiff --git a/dags/reset_data_dag.py b/dags/reset_data_dag.py[m
[1mindex 302ce04..a9c4681 100644[m
[1m--- a/dags/reset_data_dag.py[m
[1m+++ b/dags/reset_data_dag.py[m
[36m@@ -3,10 +3,10 @@[m [mfrom airflow.operators.python import PythonOperator[m
 from datetime import datetime[m
 from tasks.download import download_raw_data[m
 # from tasks.utils import unzip_file[m
[31m-from tasks.upload import drop_pg_tables [m
[32m+[m[32mfrom tasks.upload import load_x_to_pg, load_y_to_pg, drop_pg_tables[m
 [m
 with DAG([m
[31m-    dag_id='reset data',[m
[32m+[m[32m    dag_id='reset_data',[m
     description='reset raw data from Internet',[m
     tags=['Rakuten'],[m
     schedule=None,[m
[36m@@ -18,15 +18,35 @@[m [mwith DAG([m
 ) as dag:[m
     [m
     task_1 = PythonOperator([m
[31m-        task_id='drop_x_y_train_tables',[m
[32m+[m[32m        task_id='drop_former_pg_tables',[m
         python_callable=drop_pg_tables,[m
[31m-        op_kwargs={'table_names': ['x_train', 'y_train']},[m
[32m+[m[32m        op_kwargs={'table_names': ['x_train', 'y_train', 'x_test', 'y_test']},[m
     )[m
     task_2 = PythonOperator([m
         task_id='download_raw_data',[m
         python_callable=download_raw_data,[m
     )[m
     [m
[32m+[m[32m    task_3 = PythonOperator([m
[32m+[m[32m        task_id='split_x_test',[m
[32m+[m[32m        python_callable=load_x_to_pg,[m
[32m+[m[32m        op_kwargs={[m
[32m+[m[32m            'csv_path': "/opt/airflow/raw_data/x_train.csv",[m
[32m+[m[32m            'table_name': "x_test",[m
[32m+[m[32m            'start_row': 80000[m
[32m+[m[32m        }[m
[32m+[m[32m    )[m
[32m+[m[41m    [m
[32m+[m[32m    task_4 = PythonOperator([m
[32m+[m[32m        task_id='split_y_test',[m
[32m+[m[32m        python_callable=load_y_to_pg,[m
[32m+[m[32m        op_kwargs={[m
[32m+[m[32m            'csv_path': "/opt/airflow/raw_data/y_train.csv",[m
[32m+[m[32m            'table_name': "y_test",[m
[32m+[m[32m            'start_row': 80000[m
[32m+[m[32m        }[m
[32m+[m[41m        [m
[32m+[m[32m    )[m
     # task_2 = PythonOperator([m
     #     task_id='unzip_image',[m
     #     python_callable= unzip_file,[m
[36m@@ -36,4 +56,4 @@[m [mwith DAG([m
     #     }  [m
     # )[m
     [m
[31m-    task_1 >> task_2[m
\ No newline at end of file[m
[32m+[m[32m    task_1 >> task_2 >> [task_3, task_4][m
\ No newline at end of file[m
[1mdiff --git a/dags/tasks/upload.py b/dags/tasks/upload.py[m
[1mindex 102af0d..1da4f75 100644[m
[1m--- a/dags/tasks/upload.py[m
[1m+++ b/dags/tasks/upload.py[m
[36m@@ -14,15 +14,23 @@[m [mengine = create_engine("postgresql+psycopg2://rakutenadmin:rakutenadmin@postgres[m
 #     aws_access_key_id=conn.login,[m
 #     aws_secret_access_key=conn.password,[m
 # )[m
[31m-def load_x_to_pg(csv_path, table_name, num_rows):[m
[32m+[m[32mdef load_x_to_pg(csv_path, table_name,start_row=None, end_row=None):[m
     df = pd.read_csv(csv_path, skiprows=1, names=[[m
         "id", "designation", "description", "productid", "imageid"[m
     ])[m
 [m
[31m-    num_rows = min(max(num_rows, 0), len(df))[m
[31m-    df_to_import = df.iloc[:num_rows][m
[31m-    df_remaining = df.iloc[num_rows:][m
[32m+[m[32m    total_rows = len(df)[m
[32m+[m[41m    [m
[32m+[m[32m    start_row = 0 if start_row is None else max(0, start_row)[m
[32m+[m[32m    end_row = total_rows if end_row is None else min(end_row, total_rows)[m
[32m+[m
[32m+[m[32m    if start_row >= end_row:[m
[32m+[m[32m        print("Invalid row range: start_row must be less than end_row.")[m
[32m+[m[32m        return[m
 [m
[32m+[m[32m    df_to_import = df.iloc[start_row:end_row][m
[32m+[m[32m    df_remaining = pd.concat([df.iloc[:start_row], df.iloc[end_row:]], ignore_index=True)[m
[32m+[m[41m    [m
     metadata = MetaData(bind=engine)[m
 [m
     Table([m
[36m@@ -39,15 +47,26 @@[m [mdef load_x_to_pg(csv_path, table_name, num_rows):[m
     df_to_import.to_sql(table_name, engine, if_exists="append", index=False)[m
 [m
     df_remaining.to_csv(csv_path, index=False)[m
[32m+[m[41m    [m
[32m+[m[32m    print(f"Imported rows {start_row} to {end_row} ({len(df_to_import)} rows). Remaining {len(df_remaining)} rows saved to CSV.")[m
 [m
[31m-def load_y_to_pg(csv_path, table_name, num_rows):[m
[32m+[m
[32m+[m[32mdef load_y_to_pg(csv_path, table_name,start_row=None, end_row=None):[m
     df = pd.read_csv(csv_path, skiprows=1, names=[[m
         "id", "prdtypecode"[m
     ])[m
 [m
[31m-    num_rows = min(max(num_rows, 0), len(df))[m
[31m-    df_to_import = df.iloc[:num_rows][m
[31m-    df_remaining = df.iloc[num_rows:][m
[32m+[m[32m    total_rows = len(df)[m
[32m+[m[41m    [m
[32m+[m[32m    start_row = 0 if start_row is None else max(0, start_row)[m
[32m+[m[32m    end_row = total_rows if end_row is None else min(end_row, total_rows)[m
[32m+[m
[32m+[m[32m    if start_row >= end_row:[m
[32m+[m[32m        print("Invalid row range: start_row must be less than end_row.")[m
[32m+[m[32m        return[m
[32m+[m
[32m+[m[32m    df_to_import = df.iloc[start_row:end_row][m
[32m+[m[32m    df_remaining = pd.concat([df.iloc[:start_row], df.iloc[end_row:]], ignore_index=True)[m
     [m
     metadata = MetaData(bind=engine)[m
 [m
[36m@@ -56,13 +75,16 @@[m [mdef load_y_to_pg(csv_path, table_name, num_rows):[m
         Column("id", Integer, primary_key=True),[m
         Column("prdtypecode", Integer),[m
     )[m
[31m-    [m
[32m+[m
     metadata.create_all()[m
[31m-    [m
[32m+[m
     df_to_import.to_sql(table_name, engine, if_exists="append", index=False)[m
 [m
     df_remaining.to_csv(csv_path, index=False)[m
     [m
[32m+[m[32m    print(f"Imported rows {start_row} to {end_row} ({len(df_to_import)} rows). Remaining {len(df_remaining)} rows saved to CSV.")[m
[32m+[m
[32m+[m
 def drop_pg_tables(table_names: list):[m
     metadata = MetaData(bind=engine)[m
     inspector = inspect(engine)[m
