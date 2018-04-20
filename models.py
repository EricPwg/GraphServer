import datetime
import pony.orm as pny

from config import DB_NAME

database = pny.Database("sqlite", DB_NAME, create_db=True)


class AtPressure(database.Entity):
    timestamp = pny.PrimaryKey(datetime.datetime)
    value = pny.Required(float)


class CO2(database.Entity):
    timestamp = pny.PrimaryKey(datetime.datetime)
    value = pny.Required(float)


class Temperature(database.Entity):
    timestamp = pny.PrimaryKey(datetime.datetime)
    value = pny.Required(float)


class Humidity(database.Entity):
    timestamp = pny.PrimaryKey(datetime.datetime)
    value = pny.Required(float)


class WindSpeed(database.Entity):
    timestamp = pny.PrimaryKey(datetime.datetime)
    value = pny.Required(float)


class RainMeter(database.Entity):
    timestamp = pny.PrimaryKey(datetime.datetime)
    value = pny.Required(float)


class Bugs(database.Entity):
    timestamp = pny.PrimaryKey(datetime.datetime)
    value = pny.Required(float)


class UV1(database.Entity):
    timestamp = pny.PrimaryKey(datetime.datetime)
    value = pny.Required(float)


class UV2(database.Entity):
    timestamp = pny.PrimaryKey(datetime.datetime)
    value = pny.Required(float)


class UV3(database.Entity):
    timestamp = pny.PrimaryKey(datetime.datetime)
    value = pny.Required(float)


class Moisture1(database.Entity):
    timestamp = pny.PrimaryKey(datetime.datetime)
    value = pny.Required(float)


class PH1(database.Entity):
    timestamp = pny.PrimaryKey(datetime.datetime)
    value = pny.Required(float)


class Moisture2(database.Entity):
    timestamp = pny.PrimaryKey(datetime.datetime)
    value = pny.Required(float)


class PH2(database.Entity):
    timestamp = pny.PrimaryKey(datetime.datetime)
    value = pny.Required(float)


class Moisture3(database.Entity):
    timestamp = pny.PrimaryKey(datetime.datetime)
    value = pny.Required(float)


class PH3(database.Entity):
    timestamp = pny.PrimaryKey(datetime.datetime)
    value = pny.Required(float)


class Moisture4(database.Entity):
    timestamp = pny.PrimaryKey(datetime.datetime)
    value = pny.Required(float)


class PH4(database.Entity):
    timestamp = pny.PrimaryKey(datetime.datetime)
    value = pny.Required(float)

# turn on debug mode
# pny.sql_debug(True)

# map the models to the database
# and create the tables, if they don't exist
database.generate_mapping(create_tables=True)