#!/usr/bin/python
from datetime import datetime
from json import load
from typing import Text

from click import (
    Choice as CHOICE,
    File as FILE,
    Path as PATH,
    argument,
    command,
    option,
)

from loguru import logger

from peewee import Field, ForeignKeyField, Model, TextField

from playhouse.sqlite_ext import SqliteExtDatabase

from tqdm import tqdm


db = SqliteExtDatabase(None)


class TimestampTzField(Field):
    """
    A timestamp field that supports a timezone by serializing the value
    with isoformat.
    """

    field_type = "TEXT"  # This is how the field appears in Sqlite

    def db_value(self, value: datetime) -> str:
        if value:
            if isinstance(value, str):
                value = self.python_value(value)
            return value.isoformat()

    def python_value(self, value: str) -> str:
        if value:
            return datetime.fromisoformat(value)


class BaseModel(Model):
    class Meta:
        database = db


class Profile(BaseModel):
    public_display_name = TextField()
    screen_name = TextField()
    uuid = TextField(unique=True)


class Trip(BaseModel):
    start = TextField()
    display_name = TextField()
    profile = ForeignKeyField(Profile, backref="trips")


class Air(BaseModel):
    start = TextField()
    trip = ForeignKeyField(Trip, backref="airs")


class Airport(BaseModel):
    iata = TextField(unique=True)
    latitude = TextField(unique=True)
    longitude = TextField(unique=True)
    city = TextField()
    country = TextField()


class Segment(BaseModel):
    air = ForeignKeyField(Air, backref="segments")
    origin = ForeignKeyField(Airport, backref="origin")
    start = TimestampTzField()
    destination = ForeignKeyField(Airport, backref="origin")
    end = TimestampTzField()
    aircraft = TextField(null=True)
    flight = TextField(null=True)


@command()
@argument(
    "files",
    type=FILE(),
    nargs=-1,
)
@option(
    "--database",
    type=PATH(file_okay=True, dir_okay=False, allow_dash=False, resolve_path=True),
    default="tripit.db",
)
@option(
    "--log-level",
    type=CHOICE(
        ["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG", "SUCCESS", "TRACE"],
        case_sensitive=False,
    ),
    default="INFO",
)
@option("-s", "--silent", is_flag=True, help="Don't show progress bar")
def cli(
    files,
    database,
    log_level,
    silent,
):
    # Initialise Logger
    logger.remove()
    logger.add(lambda msg: tqdm.write(msg, end=""), level=log_level)

    # Initialise Database
    db.init(
        database,
        pragmas={"cache_size": -64 * 1000, "synchronous": 0, "foreign_keys": 1},
    )
    db.connect()
    db.create_tables([Profile, Trip, Air, Segment, Airport])
    db.execute_sql(
        """
        CREATE VIEW airport_view AS
            select
                airport.iata,
                airport.latitude,
                airport.longitude,
                airport.city,
                airport.country,
                (SELECT COUNT(id) as numorigin from segment where segment.origin_id = airport.id) +
                (SELECT COUNT(id) as numorigin from segment where segment.destination_id = airport.id) total
            from
                airport
            order by
                total desc
        """
    )
    db.execute_sql(
        """
        CREATE VIEW segment_view AS
            select
                a1.iata as iata_1,
                a2.iata as iata_2,
                r.count
            from
                (
                    select
                        case
                            when origin_id < destination_id then origin_id
                            else destination_id
                        end as airport1_id,
                        case
                            when origin_id < destination_id then destination_id
                            else origin_id
                        end as airport2_id,
                        count(id) as [count]
                    from
                        segment
                    group by
                        airport1_id,
                        airport2_id
                ) as r
                join airport as a1 on r.airport1_id = a1.id
                join airport as a2 on r.airport2_id = a2.id
            order by
                [count] desc
        """
    )

    for file in files:
        json_data = load(file)

        with db.atomic():
            for json_profile in tqdm(
                json_data["profiles"],
                unit="profiles",
                disable=silent,
                leave=False,
            ):
                sql_profile, created = Profile.get_or_create(
                    public_display_name=json_profile["public_display_name"],
                    screen_name=json_profile["screen_name"],
                    uuid=json_profile["uuid"],
                )

                if created:
                    logger.info(f" - Added Profile {sql_profile}")

                for json_trip in tqdm(
                    json_profile["trips"],
                    unit="trips",
                    disable=silent,
                    leave=False,
                ):
                    sql_trip, created = Trip.get_or_create(
                        profile=sql_profile,
                        start=json_trip["start"],
                        display_name=json_trip["display_name"],
                        defaults={},
                    )

                    if created:
                        logger.info(f"  - Added Trip {sql_trip}")

                    for json_air in tqdm(
                        json_trip["airs"],
                        unit="airs",
                        disable=silent,
                        leave=False,
                    ):
                        sql_air, created = Air.get_or_create(
                            trip=sql_trip,
                            start=json_air["start"],
                            defaults={},
                        )
                        if created:
                            logger.info(f"   - Added Air {sql_air}")

                        for json_segment in tqdm(
                            json_air["segments"],
                            unit="segments",
                            disable=silent,
                            leave=False,
                        ):
                            sql_origin, created = Airport.get_or_create(
                                iata=json_segment["origin"]["iata"],
                                defaults={
                                    "latitude": json_segment["origin"]["latitude"],
                                    "longitude": json_segment["origin"]["longitude"],
                                    "city": json_segment["origin"]["city"],
                                    "country": json_segment["origin"]["country"],
                                },
                            )
                            if created:
                                logger.info(f"    - Added Airport {sql_origin}")

                            sql_destination, created = Airport.get_or_create(
                                iata=json_segment["destination"]["iata"],
                                defaults={
                                    "latitude": json_segment["destination"]["latitude"],
                                    "longitude": json_segment["destination"][
                                        "longitude"
                                    ],
                                    "city": json_segment["destination"]["city"],
                                    "country": json_segment["destination"]["country"],
                                },
                            )
                            if created:
                                logger.info(f"    - Added Airport {sql_destination}")

                            sql_segment, created = Segment.get_or_create(
                                air=sql_air,
                                start=json_segment["start"],
                                end=json_segment["end"],
                                defaults={
                                    "destination": sql_destination,
                                    "origin": sql_origin,
                                    "aircraft": json_segment.get("aircraft"),
                                    "flight": json_segment.get("flight"),
                                },
                            )
                            if created:
                                logger.info(f"    - Added Segment {sql_segment}")


if __name__ == "__main__":
    cli()
