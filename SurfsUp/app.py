# Dependencies
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify


# Database Setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save reference to the table
measurement = Base.classes.measurement
station = Base.classes.station

# Flask Setup
app = Flask(__name__)

# Flask Routes

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"<h2>Module 10 Climate App<h2><br/>"
        f"Available Routes are:<br/>"
        f"<ul><li>Precipitation - <code>/api/v1.0/precipitation<code><li><ul>"
        f"<ul><li>Stations - <code>/api/v1.0/stations<code><li><ul>"
        f"<ul><li>Temperatures - <code>/api/v1.0/tobs<code><li><ul>"
        f"<ul><li>Temperatures After Date - <code>/api/v1.0/start<code><li><ul>"
        f"<ul><li>Temperatures in Date Range - <code>/api/v1.0/start/end<code><li><ul>"
    )

# Date Info
recentMost = session.query(measurement.date).order_by(measurement.date.desc()).first()[0]
year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query last 12 months of precipitation data
    data = [measurement.date, measurement.prcp]
    results = session.query(*data).filter(measurement.date.between(str(year), recentMost)).all()

    # Create Dictionary to return as json
    precip_list = []
    
    for date,prcp in results:
        precip_dict = {}
        precip_dict[date] = prcp
        precip_list.append(precip_dict)

    session.close()

    return jsonify(precip_list)


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query for all stations
    results = session.query(station.station).distinct().all()

    # Create List for json
    stations = list(np.ravel(results))

    session.close()

    # Return json
    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query most active station
    active = session.query(measurement.station,func.count(measurement.station)).group_by(measurement.station).\
        order_by(func.count(measurement.station).desc()).all()
    most_active = active[0][0]


    # Query for temps in recent year at most active station
    act_year_query = session.query(measurement.date,measurement.tobs)\
                .filter(measurement.station==most_active)\
                .filter(measurement.date.between(str(year), recentMost)).all()
    
    # Create Dictionary to return as json
    tobs_list = []
    
    for date,tobs in act_year_query:
        tobs_dict = {}
        tobs_dict[date] = tobs
        tobs_list.append(tobs_dict)

    session.close()

    return jsonify(tobs_list)


@app.route("/api/v1.0/start")
def one_date(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Min, Max, Avg in Date Range w variable Start
    info = [func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)]
    query = session.query(*info).filter(measurement.date.between(start, recentMost)).all()

    session.close()

    return(
        f"Min temp: {query[0]}"
        f"Max temp: {query[1]}"
        f"Avg temp: {query[2]}"
    )

@app.route("/api/v1.0/start/end")
def two_date(start, end):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Min, Max, Avg in Variable Date Range
    info = [func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)]
    query = session.query(*info).filter(measurement.date.between(start, end)).all()

    session.close()

    return(
        f"Min temp: {query[0]}"
        f"Max temp: {query[1]}"
        f"Avg temp: {query[2]}"
    )

if __name__ == '__main__':
    app.run(debug=True)