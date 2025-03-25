# 🌤️ Openweathermap_ETL_pipeline
## A beginner-friendly data engineering project that collects and stores daily weather data from various cities around the world.This project uses Apache Airflow, PostgreSQL, Docker, and the OpenWeatherMap API to automate the data pipeline.

## Architecture
![image](https://github.com/user-attachments/assets/651b1a9f-a820-4a68-8612-fee2948761a6)

## 🔧 Technologies Used
 Apache Airflow – to schedule and orchestrate the daily pipeline

 PostgreSQL – to store weather data

 Docker / Docker Compose – to containerize the entire setup

 OpenWeatherMap API – as the data source

 Python 
## 📁 Project Structure

## ⚙️ How It Works

An Airflow DAG runs once per day

It fetches current weather data for 10 major cities (e.g., Berlin, London, Tokyo)

The data is transformed and inserted into a PostgreSQL table

The table includes a UNIQUE constraint on (date, city) to prevent duplicates

## 🚀 Getting Started
# 1.Clone the repository:
git clone https://github.com/athi2210/openweathermap_ETL_pipeline.git \\

cd openweathermap_ETL_pipeline
# 2.Openweather Api
Aquire your own API_KEY on the openweather site and replace the placeholder in the pythonfile with your Key
# 3.Start Docker containers:
docker compose up airflow-init

docker-compose up --d
# 4.Access Airflow:
URL: http://localhost:8080 \\

Default login: airflow / airflow
# 5 Setup the airflow Postgres Connection
In order to store the pulled values into your postgres database, you have to setup the connetion in Airflow

a)You setup the connection press on Admin -> Connections

b)Fillout the form

![image](https://github.com/user-attachments/assets/6885e5bb-bd56-41d0-9feb-cc1f3f04c05b)

