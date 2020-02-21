# Dependencies
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect

from flask import Flask, jsonify

import datetime
from dateutil import parser
import dateutil as du
from dateutil.relativedelta import relativedelta

import os

#################################################
# Database Setup
#################################################
# | 01 | √ | Correctly generates the engine to the correct sqlite file 

# Assign location of this file:
script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
rel_path = "hawaii.sqlite"
abs_file_path = os.path.join(script_dir, rel_path)
print(abs_file_path)

engine = sqlalchemy.create_engine("sqlite:///hawaii.sqlite", echo=True)
connection = engine.connect()
metadata = sqlalchemy.MetaData()
print(metadata)
#census = db.Table('census', metadata, autoload=True, autoload_with=engine)

# reflect an existing database into a new model
# | 02 | √ | Uses automap_base() and reflects the database schema
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Create the inspector and connect it to the engine
inspector = inspect(engine)

# Collect the names of tables within the database
print(inspector.get_table_names())