import os
from dataclasses import dataclass
from pytz import timezone

from dotenv import load_dotenv


@dataclass
class DatabaseConfig:
    host: str
    port: str
    password: str
    user: str
    database: str

    @property
    def conn_string(self):
        return 'postgresql://{user}:{password}@{location}:{port}/{db_name}'.format(user=self.user,
                                                                                   password=self.password,
                                                                                   location=self.host,
                                                                                   port=self.port,
                                                                                   db_name=self.database)

    @property
    def async_conn_string(self):
        return 'postgresql+asyncpg://{user}:{password}@{location}:{port}/{db_name}'.format(user=self.user,
                                                                                           password=self.password,
                                                                                           location=self.host,
                                                                                           port=self.port,
                                                                                           db_name=self.database)


@dataclass
class Miscellaneous:
    time_zone: timezone
    secret: str = None
    other_params: str = None


@dataclass
class Config:
    db: DatabaseConfig
    misc: Miscellaneous


def load_config(env_file: str = '.env'):
    load_dotenv(dotenv_path=env_file)

    return Config(
        db=DatabaseConfig(
            host=str(os.environ["POSTGRES_LOCATION"]),
            password=str(os.environ["POSTGRES_PASSWORD"]),
            user=str(os.environ["POSTGRES_USER"]),
            database=str(os.environ["POSTGRES_DB"]),
            port=str(os.environ["POSTGRES_PORT"])
        ),
        misc=Miscellaneous(time_zone=timezone(str(os.environ["TIME_ZONE"])),
                           secret=str(os.environ["SECRET_KEY"]))
    )


if __name__ == '__main__':
    pass
