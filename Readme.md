This is a simple webservice to store you log data from you project.

You need to set your environment variables in .env file:<br>
POSTGRES_USER=logger_user
POSTGRES_PASSWORD=1234567890qwerty
POSTGRES_DB=logging_server
POSTGRES_LOCATION=logger_server_db_1
POSTGRES_PORT=5432

TIME_ZONE=Europe/Moscow
SECRET_KEY=thisisaverysecretkey

And run it with:
docker-compose up --env-file .env up -d

Default port for service is 8002 and for database is 5433
<br>
For client log configuration you can check examples folder
