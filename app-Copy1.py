# Dependencies
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

import datetime
from dateutil import parser
import dateutil as du
from dateutil.relativedelta import relativedelta

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
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
    """List all available api routes."""
    return (
        f"Available Routes: <br />"
        f"<a href='/api/v1.0/precipitation'>/api/v1.0/precipitation'></a> <br />"
        f"<a href='/api/v1.0/stations'>/api/v1.0/stations</a> <br />"
        f"<a href='/api/v1.0/tobs'>/api/v1.0/tobs</a> <br />"
        f"<a href='/api/v1.0/2017-08-01'>/api/v1.0/(start in YYYY-MM-DD format)</a> <br />" # Max datetime value in date column: 2017-08-23 00:00:00
        f"<a href='/api/v1.0/2017-08-01/2017-08-09'>/api/v1.0/(start in YYYY-MM-DD format)/(end in YYYY-MM-DD format)</a> <br />"
    )

# | 3 | | **Route "/api/v1.0/precipitation"** - Convert the query results to a Dictionary using **date** as the key and **prcp** as the value.
# | 4 | | Return the JSON representation of your dictionary.
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query all data
    sel = [Measurement.date, Measurement.prcp]
    results = session.query(*sel).all()

    session.close()

    # Convert list of tuples into normal list
    all_data = list(np.ravel(results))

    # return a json version:
    return jsonify(all_data)

# | 5 | | **Route "/api/v1.0/stations"** - Return a JSON list of stations from the dataset
@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query all data
    sel = [Station.station]
    results = session.query(*sel).all()

    session.close()

    # Convert list of tuples into normal list
    all_data = list(np.ravel(results))

    # return a json version:
    return jsonify(all_data)

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

    # Get the latest date in the dataset, then go back 12 full months
    max_dt = session.query(func.max(Measurement.date)).scalar()

    # Get the data into datetime format so we can use in an operator
    new_max_dt = parser.parse(max_dt)  # datetime.datetime(1999, 8, 28, 0, 0)

    twelve_months = new_max_dt + relativedelta(months=-12)

    # Return tobs for most active station
    # | 6 | √ | **Route "/api/v1.0/tobs"** - query for the dates and temperature observations from a year from the last data point.
    results = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date >= twelve_months).\
        all()

    #####################################################
    # Copy and paste from the other activity ^ end
    #####################################################

    session.close()

    # Convert list of tuples into normal list
    all_data = list(np.ravel(results))

    # return a json version:
    # | 7 | √ | Return a JSON list of Temperature Observations (tobs) for the previous year.
    return jsonify(all_data)


####################################################################################
# Start+
####################################################################################
@app.route("/api/v1.0/<start>")
def start_only(start):
    # Validate date format:
    try:
        new_start = datetime.datetime.strptime(start, '%Y-%m-%d')
    except ValueError:
        return jsonify({"error": f"Incorrect date format - should be YYYY-MM-DD"}), 500

    # Create our session (link) from Python to the DB
    session = Session(engine)

    sel = [
        func.min(Measurement.tobs)
        , func.max(Measurement.tobs)
        , func.avg(Measurement.tobs)
    ]

    results = session.query(*sel).\
        filter(Measurement.date >= new_start).\
        all()

    session.close()

    # Convert list of tuples into normal list
    all_data = list(np.ravel(results))

    # return a json version:
    # | 8 | | **Route "/api/v1.0/(start)"** - Return a JSON list of the minimum temperature, the average temperature, 
    # #             and the max temperature for a given start without an end. 
    # "When given the start only, calculate TMIN, TAVG, and TMAX for **all dates greater than and equal to the start date**."
    return jsonify(all_data)

####################################################################################
# Start+End
####################################################################################
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

    sel = [
        func.min(Measurement.tobs)
        , func.max(Measurement.tobs)
        , func.avg(Measurement.tobs)
    ]

    # | 9 | √ | **Route "/api/v1.0/(start)/(end)"** - "When given the start and the end date, 
    # calculate the TMIN, TAVG, and TMAX for dates between the start and end date **inclusive**."
    results = session.query(*sel).\
        filter(Measurement.date >= new_start, Measurement.date <= new_end).\
        all()

    session.close()

    # Convert list of tuples into normal list
    all_data = list(np.ravel(results))

    # return a json version:
    return jsonify(all_data)


################################################################
# Final     

if __name__ == '__main__':
    app.run(debug=True)