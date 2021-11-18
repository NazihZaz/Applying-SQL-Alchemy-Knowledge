# Import dependecies
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import numpy as np

# create engine to hawaii.sqlite
database_path="Resources/hawaii.sqlite"
engine = create_engine(f"sqlite:///{database_path}")

# reflect an existing database into a new model
Base=automap_base()

# reflect the tables
Base.prepare(engine,reflect=True)

# Save references to each table
Measurement=Base.classes.measurement
Station=Base.classes.station

# Import Flask
from flask import Flask, jsonify

# Flask setup
app=Flask(__name__)

# Flask routes
@app.route("/")
def home():
    """List all available api routes"""
    return (
            f"Welcome to Nazih Bouanani's API Home Page<br/>"
            f"Data Available between 2010-01-01 and2017-08-23"
            f"Here are the available Routes:<br/>"
            f"/api/v1.0/precipitation<br/>"
            f"/api/v1.0/stations<br/>"
            f"/api/v1.0/tobs<br/>"
            f"/api/v1.0/start<br/>"
            f"/api/v1.0/start/end<br/>"
            )

@app.route("/api/v1.0/precipitation")
def prcp():
    """Redirected to the Precipitation Page"""
     
    # Create our session (link) from Python to the DB
    session=Session(engine) 
    
    # Query all precipitations for Hawaii
    max_precipitation=session.query(Measurement.date,func.max(Measurement.prcp)).filter(Measurement.date>="2016-08-23").\
        group_by(Measurement.date).all()

    # Close the session
    session.close()

    # Create a dictionary from the row data and append to a list of all_prcp
    all_prcp = []
    
    for date, prcp in max_precipitation:
        all_prcp.append({date:prcp})
    
    # Jsponify the list
    return jsonify(all_prcp)

@app.route("/api/v1.0/stations")
def stations():
    """Redirected to the Station Page"""
    
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    # Query all stations
    no_stations=session.query(Station.name).all()

    # Close the session
    session.close()

    # Convert list of tuples into normal list
    all_stations = list(np.ravel(no_stations))

    # Jsonify the list
    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    """Redirected to the Temperature of Observation Page"""
    
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    # Query all temperatures
    year_temperatures=session.query(Measurement.date,Measurement.tobs).\
    filter(Measurement.station=="USC00519281").\
    filter(Measurement.date>="2016-08-23").all()

    # Close the session
    session.close()
    
    # Create a dictionary from the row data and append to a list of all_tobs
    all_tobs=[]
        
    for date, tobs in year_temperatures:
        date
        tobs
        all_tobs.append({date:tobs})

    # Jsonify the list
    return jsonify(all_tobs)

@app.route("/api/v1.0/<start>")
def temperatures_start(start):
    """Fetch the minimun, average and maximum temperature for the dates
       greater or equal to the start date, or a 404 if not."""
        
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    # Query the min, max and average temperatures
    sel=[Measurement.date,func.min(Measurement.tobs),func.max(Measurement.tobs), func.avg(Measurement.tobs)]
    temperatures=session.query(*sel).filter(Measurement.date>=start).all()
    
    # Query all the dates within the database
    dates=session.query(Measurement.date).all()
    
    # Close the session   
    session.close()
    
    # Convert list of tuples into normal list
    all_dates=list(np.ravel(dates))
    
    #  Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start 
    for start_date in all_dates:
        if start_date==start:
            for date,tmin,tmax,tavg in temperatures:
                return jsonify([{"Start Date": start, "End Date": "2017-08-23", "Temperature Minimum": tmin, "Temperature Average": round(tavg,1), "Temperature Maximum": tmax}])
    return jsonify([f"error: Data between '{start}' and '2017-08-23' was not found. Make sure the date format is 'YYYY-MM-DD' and within the following date range ('2010-01-01' and '2017-08-23')"]), 404

@app.route("/api/v1.0/<start>/<end>")
def temperatures_end(start,end):
    """Fetch the minimun, average and maximum temperature for the dates
       greater or equal to the start date and lesser or equal to the end date, or a 404 if not."""
        
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    # Query all temperatures
    sel=[Measurement.date,func.min(Measurement.tobs),func.max(Measurement.tobs), func.avg(Measurement.tobs)]
    temperatures=session.query(*sel).filter(Measurement.date>=start).filter(Measurement.date<=end).all()
    
    # Query all the dates within the database
    dates=session.query(Measurement.date).all()
    
    # Close the session   
    session.close()
    
    # Convert list of tuples into normal list
    all_dates=list(np.ravel(dates))
     
    for start_date in all_dates:
        for end_date in all_dates:
            if start_date==start and end_date==end:
                for date,tmin,tmax,tavg in temperatures:
                    return jsonify([{"Start Date": start, "End Date": end, "Temperature Minimum": tmin, "Temperature Average": round(tavg,1), "Temperature Maximum": tmax}])
        return jsonify([f"error: Data between '{start}' and '{end}' was not found. Make sure the date format is 'YYYY-MM-DD' and within the following date range ('2010-01-01' and '2017-08-23'). "
                    f"When enterring the endpoint, make sure the start date is enterred first and the end date is enterred last"]), 404
    return jsonify([f"error: Data between '{start}' and '{end}' was not found. Make sure the date format is 'YYYY-MM-DD' and within the following date range ('2016-08-23' and '2017-08-23'). "
                    f"When enterring the endpoint, make sure the start date is enterred first and the end date is enterred last"]), 404

if __name__ == '__main__':
    app.run(debug=True)