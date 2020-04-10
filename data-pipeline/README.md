
### Local Development
```shell script
docker build --rm --build-arg AIRFLOW_DEPS="aws" -t puckel/docker-airflow .
```

```shell script
docker run --name sw-airflow \
-v $(pwd)/airflow-requirements.txt:/usr/local/airflow/requirements.txt \
-v $(pwd)/dags:/usr/local/airflow/dags \
-d -p 8080:8080 puckel/docker-airflow:1.10.9 webserver
```

on windows:
```cmd
docker run --name sw-airflow ^
-v "C:\Users\...\spiderweb\data-pipeline\airflow-requirements.txt":/usr/local/airflow/requirements.txt ^
-v "C:\Users\...\spiderweb\data-pipeline\dags":/usr/local/airflow/dags ^
-d -p 8080:8080 puckel/docker-airflow:latest webserver
```