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

#################################################
# Database Setup
#################################################
# | 01 | √ | Correctly generates the engine to the correct sqlite file 
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
# | 02 | √ | Uses automap_base() and reflects the database schema
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Create the inspector and connect it to the engine
inspector = inspect(engine)

# Collect the names of tables within the database
inspector.get_table_names()

# Using the inspector to print the column names within the 'dow' table and its types
columns = inspector.get_columns('dow')
for column in columns:
    print(column["name"], column["type"])

# Save references to each table
# | 03 | √ | Correctly saves references to the tables in the sqlite file (measurement and station)
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

# | 1 | √ | **Route "\"** - home page
# | 2 | √ | List all routes available
@app.route("/")
def welcome():
    "<h1>""List all available api routes.""</h1>"
    return (
        f"Available Routes: <br />"
        f"<a href='/api/v1.0/precipitation'>/api/v1.0/precipitation</a> <br />"
        f"<a href='/api/v1.0/stations'>/api/v1.0/stations</a> <br />"
        f"<a href='/api/v1.0/tobs'>/api/v1.0/tobs</a> <br />"
        f"<a href='/api/v1.0/2017-08-01'>/api/v1.0/2017-08-01</a> <br />" # Max datetime value in date column: 2017-08-23 00:00:00
        f"<a href='/api/v1.0/2017-08-01/2017-08-09'>/api/v1.0/2017-08-01/2017-08-09</a> <br />"
    )

# | 3 | | **Route "/api/v1.0/precipitation"** - Convert the query results to a Dictionary using **date** as the key and **prcp** as the value.
# | 4 | | Return the JSON representation of your dictionary.
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    # | 04 | √ | Correctly creates and binds the session between the python app and database
    session = Session(engine)

    #####################################################
    # Copy and paste from the other activity:
    #####################################################
    # Get the latest date in the dataset, then go back 12 full months
    max_dt = session.query(func.max(Measurement.date)).scalar()

    # Get the data into datetime format so we can use in an operator
    new_max_dt = parser.parse(max_dt)  # datetime.datetime(1999, 8, 28, 0, 0)

    twelve_months = new_max_dt + relativedelta(months=-12)

    # Slice out the columns you need: prcp and date
    sel = [Measurement.date, Measurement.prcp]

    # Query the dataset and put into variable
    results = session.query(*sel).filter(Measurement.date >= twelve_months).all()

    session.close()

    # return a json version:
    # | 01 | | Returns the **jsonified** precipitation data for the last year in the database
    # | 02 | | Returns json with the **date as the key** and the **value as the precipitation**
    return jsonify(results)

# | 5 | | **Route "/api/v1.0/stations"** - Return a JSON list of stations from the dataset
@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query all data
    sel = [Station.station]
    results = session.query(*sel).all()

    session.close()

    # return a json version:
    # | 01 | √ | Returns jsonified data of all of the stations in the database
    return jsonify(results)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    #####################################################
    # Copy and paste from the other activity:
    #####################################################
    
    # What stations have the most rows?
    sel = [Measurement.station, func.count(Measurement.tobs)]

    activestations = session.query(*sel).\
        group_by(Measurement.station).\
        order_by(func.count(Measurement.tobs).desc()).all()

    # Get the most active station
    most_active = str(activestations[0][0]) 

    # Get the latest date in the dataset, then go back 12 full months
    max_dt = session.query(func.max(Measurement.date)).scalar()

    # Get the data into datetime format so we can use in an operator
    new_max_dt = parser.parse(max_dt)  # datetime.datetime(1999, 8, 28, 0, 0)

    twelve_months = new_max_dt + relativedelta(months=-12)
    
    # Return tobs for most active station
    # | 6 | √ | **Route "/api/v1.0/tobs"** - query for the dates and temperature observations from a year from the last data point.
    # | 01 | √ | Returns jsonified data for the most active station (USC00519281) for the last year of data
    results = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.station == most_active, Measurement.date >= twelve_months).\
        all()

    #####################################################
    # Copy and paste from the other activity ^ end
    #####################################################

    session.close()

    # return a json version:
    # | 7 | √ | Return a JSON list of Temperature Observations (tobs) for the previous year.
    return jsonify(results)


####################################################################################
# Start+
####################################################################################
# | 01 | √ | Route accepts the start date as a parameter from the URL
@app.route("/api/v1.0/<start>")
def start_only(start):
    # Validate date format:
    try:
        new_start = datetime.datetime.strptime(start, '%Y-%m-%d')
    except ValueError:
        return jsonify({"error": f"Incorrect date format - should be YYYY-MM-DD"}), 500

    # Create our session (link) from Python to the DB

    # | 02 | √ | Returns the min, max, and average temperatures calculated from the given start date to the end of the dataset
    session = Session(engine)

    # Add min(date) and max(date) to show range
    sel = [
        func.min(Measurement.date)
        , func.max(Measurement.date)
        , func.min(Measurement.tobs)
        , func.max(Measurement.tobs)
        , func.avg(Measurement.tobs)
    ]

    results = session.query(*sel).\
        filter(Measurement.date >= new_start).\
        all()

    session.close()

    # return a json version:
    # | 8 | | **Route "/api/v1.0/(start)"** - Return a JSON list of the minimum temperature, the average temperature, 
    # #             and the max temperature for a given start without an end. 
    # "When given the start only, calculate TMIN, TAVG, and TMAX for **all dates greater than and equal to the start date**."
    return jsonify(results)

####################################################################################
# Start+End
####################################################################################
# | 01 | √ | Route accepts the start and end dates as parameters from the URL
@app.route("/api/v1.0/<start>/<end>")
def start_and_end(start, end):
    # Validate date format:
    try:
        new_start = datetime.datetime.strptime(start, '%Y-%m-%d')
    except ValueError:
        return jsonify({"error": f"Incorrect start date format - should be YYYY-MM-DD"}), 500
        
    try:
        new_end = datetime.datetime.strptime(end, '%Y-%m-%d')
    except ValueError:
        return jsonify({"error": f"Incorrect end date format - should be YYYY-MM-DD"}), 500

    # Create our session (link) from Python to the DB
    session = Session(engine)

    
    # | 02 | √ | Returns the min, max, and average temperatures calculated from the given start date to the end date (inclusive)

    # Add min(date) and max(date) to show range
    sel = [
        func.min(Measurement.date)
        , func.max(Measurement.date)
        , func.min(Measurement.tobs)
        , func.max(Measurement.tobs)
        , func.avg(Measurement.tobs)
    ]

    # | 9 | √ | **Route "/api/v1.0/(start)/(end)"** - "When given the start and the end date, 
    # calculate the TMIN, TAVG, and TMAX for dates between the start and end date **inclusive**."
    results = session.query(*sel).\
        filter(Measurement.date >= new_start, Measurement.date <= new_end).\
        all()

    session.close()

    # return a json version:
    return jsonify(results)


################################################################
# Final     

if __name__ == '__main__':
    app.run(debug=True)
