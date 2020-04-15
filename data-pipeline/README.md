
### Local Development
```shell script
docker build --rm --build-arg AIRFLOW_DEPS="aws" -t puckel/docker-airflow .
```

```shell script
docker-compose up -d
```