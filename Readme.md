This is a simple webservice to store you log data from you project.

You need to set your environment variables in .env file:<br>
POSTGRES_USER=logger_user<br>
POSTGRES_PASSWORD=1234567890qwerty<br>
POSTGRES_DB=logging_server<br>
POSTGRES_LOCATION=logger_server_db_1<br>
POSTGRES_PORT=5432

TIME_ZONE=Europe/Moscow<br>
SECRET_KEY=thisisaverysecretkey

And run it with:
docker-compose --env-file .env up -d

Default ports are: 8002 for service and 5433 for database<br>
For client log configuration you can check examples folder
