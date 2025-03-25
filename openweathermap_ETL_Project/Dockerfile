
# Verwendet das bestehende Airflow-Image als Basis
FROM apache/airflow:2.10.5

# Wechsle zum root-Benutzer, falls systemweite Abhängigkeiten benötigt werden
USER root

# Optional: Installiere systemweite Abhängigkeiten (z.B. falls nötig)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Zurück zum airflow-Benutzer
USER airflow

# Kopiere requirements.txt ins Docker-Image
COPY requirements.txt .

# Installiere Python-Pakete aus requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
