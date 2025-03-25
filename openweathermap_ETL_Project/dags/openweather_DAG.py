from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
import requests
import psycopg2

default_args = {
    'owner': 'athi',
    'retries': 5,
    'retry_delay': timedelta(minutes=2)
}

cities = ["Berlin", "Peking", "London", "Paris", "Tokyo", "New York", "Moskau", "Neu Dehli", "Brasilia", "Jakarta"]

def get_api(city):
    try:
        response = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={city}&lang=de&APPID=YOUR_API_KEY&units=metric"
        ).json()

        transf_dict = {
            "stadt": response["name"],
            "temp": response["main"]["temp"],
            "humidity": response["main"]["humidity"],
            "wind": response["wind"]["speed"],
            "weather_des": response["weather"][0]["description"],
            "timestamp_date": datetime.utcfromtimestamp(response["dt"]).date().isoformat(),
            "timestamp_time": datetime.utcfromtimestamp(response["dt"]).strftime("%H:%M:%S"),
            "sunrise": datetime.utcfromtimestamp(response["sys"]["sunrise"]).strftime("%H:%M:%S"),
            "sunset": datetime.utcfromtimestamp(response["sys"]["sunset"]).strftime("%H:%M:%S")
        }

        # DB-Verbindung
        conn = psycopg2.connect(
            host='host.docker.internal',
            dbname='test',
            user='airflow',
            password='airflow',
            port=5432
        )
        cursor = conn.cursor()

        insert_query = '''
            INSERT INTO weather_table (
                dt, time, city, temp, humidity, wind, weather_desc, sunrise, sunset
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        '''

        values = (
            transf_dict["timestamp_date"],
            transf_dict["timestamp_time"],
            transf_dict["stadt"],
            transf_dict["temp"],
            transf_dict["humidity"],
            transf_dict["wind"],
            transf_dict["weather_des"],
            transf_dict["sunrise"],
            transf_dict["sunset"]
        )

        cursor.execute(insert_query, values)
        conn.commit()
        cursor.close()
        conn.close()
        print(f"[✓] Wetterdaten für {city} erfolgreich gespeichert")

    except Exception as e:
        print(f"[!] Fehler bei {city}: {e}")


with DAG(
    dag_id='as30',
    default_args=default_args,
    start_date=datetime(2025, 3, 11),
    schedule_interval='@daily',
    catchup=False
) as dag:

    task1 = SQLExecuteQueryOperator(
        task_id='create_weather_table',
        conn_id='postgres_localhost',
        sql="""
            CREATE TABLE IF NOT EXISTS weather_table (
                id SERIAL PRIMARY KEY,
                dt DATE,
                time TIME,
                city VARCHAR(50),
                temp FLOAT,
                humidity FLOAT,
                wind FLOAT,
                weather_desc VARCHAR(50),
                sunrise TIME,
                sunset TIME
            )
        """
    )

    task2 = PythonOperator.partial(
        task_id="get_api",
        python_callable=get_api,
    ).expand(op_args=[[city] for city in cities])

    task1 >> task2
