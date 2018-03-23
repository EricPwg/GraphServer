import datetime
import pony.orm as pny
 
database = pny.Database("sqlite",
                        "graphdata.db",
                        create_db=True)
 
########################################################################
class Input1(database.Entity):
    timestamp = pny.PrimaryKey(datetime.datetime)
    value = pny.Required(float)
 
########################################################################
class Input2(database.Entity):
    timestamp = pny.PrimaryKey(datetime.datetime)
    value = pny.Required(float)
 
########################################################################
class Input3(database.Entity):
    timestamp = pny.PrimaryKey(datetime.datetime)
    value = pny.Required(float)
 
########################################################################
class Input4(database.Entity):
    timestamp = pny.PrimaryKey(datetime.datetime)
    value = pny.Required(float)
 
########################################################################
class Input5(database.Entity):
    timestamp = pny.PrimaryKey(datetime.datetime)
    value = pny.Required(float)
'''
########################################################################
class Input6(database.Entity):
    timestamp = pny.PrimaryKey(datetime.datetime)
    value = pny.Required(float)
 
########################################################################
class Input7(database.Entity):
    timestamp = pny.PrimaryKey(datetime.datetime)
    value = pny.Required(float)
 
########################################################################
class Input8(database.Entity):
    timestamp = pny.PrimaryKey(datetime.datetime)
    value = pny.Required(float)
 
########################################################################
class Input9(database.Entity):
    timestamp = pny.PrimaryKey(datetime.datetime)
    value = pny.Required(float)
 
########################################################################
class Input10(database.Entity):
    timestamp = pny.PrimaryKey(datetime.datetime)
    value = pny.Required(float)
 
########################################################################
 '''
# turn on debug mode
#pny.sql_debug(True)
 
# map the models to the database 
# and create the tables, if they don't exist
database.generate_mapping(create_tables=True)