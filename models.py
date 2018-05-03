import datetime
import pony.orm as pny

from config import DB_NAME

database = pny.Database("sqlite", DB_NAME, create_db=True)


class CO2(database.Entity):
    timestamp = pny.PrimaryKey(datetime.datetime)
    field = pny.Required(str)
    value = pny.Required(float)


class Humidity(database.Entity):
    timestamp = pny.PrimaryKey(datetime.datetime)
    field = pny.Required(str)
    value = pny.Required(float)


class O2(database.Entity):
    timestamp = pny.PrimaryKey(datetime.datetime)
    field = pny.Required(str)
    value = pny.Required(float)


class Temperature(database.Entity):
    timestamp = pny.PrimaryKey(datetime.datetime)
    field = pny.Required(str)
    value = pny.Required(float)


class WatchingDog(database.Entity):
    timestamp = pny.PrimaryKey(datetime.datetime)
    field = pny.Required(str)
    value = pny.Required(float)


class WaterLevel(database.Entity):
    timestamp = pny.PrimaryKey(datetime.datetime)
    field = pny.Required(str)
    value = pny.Required(float)



# turn on debug mode
# pny.sql_debug(True)

# map the models to the database
# and create the tables, if they don't exist
database.generate_mapping(create_tables=True)