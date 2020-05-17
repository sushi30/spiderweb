This module is part of the [Spiderweb](../) project. It creates local databases for testing local integrations.

### Local Development

Requirements:
- docker
- docker-compose

Copy .env.example and modify it as needed:
```commandline
cp .env.example .env
```

run the docker-compose template:
```commandline
docker-compose up
```

starting alembic
```shell script
alembic upgrade head
```

create new migration:
```shell script
alembic revision --autogenerate -m "create table_name"
```