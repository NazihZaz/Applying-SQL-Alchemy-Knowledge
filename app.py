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
def Home():
    """List all available api routes"""
    return (
            f"Welcome to Nazih Bouanani's API Home Page<br/>"
            f"Here are the available Routes:<br/>"
            f"/api/v1.0/precipitation<br/>"
            f"/api/v1.0/stations<br/>"
            f"/api/v1.0/tobs<br/>"
            f"/api/v1.0/<start><br/>"
            f"/api/v1.0/<start>/<end><br/>"
            )

@app.route("/api/v1.0/precipitation")
def Prcp():
    """Redirected to the Precipitation Page"""
     
    # Create our session (link) from Python to the DB
    session=Session(engine) 
    
    # Query all precipitations for Hawaii 8/23/2016-8/23/2017
    max_precipitation=session.query(Measurement.date,func.max(Measurement.prcp)).filter(Measurement.date>="2016-08-23").group_by(Measurement.date).all()

    # Close the session
    session.close()

    # Create a dictionary from the row data and append to a list of precipitations
    all_prcp = []
    for date, prcp in max_precipitation:
        prcp_dict = {}
        prcp_dict["Date"] = date
        prcp_dict["Precipitation"] = prcp
        all_prcp.append(prcp_dict)
    
    return jsonify(all_prcp)

@app.route("/api/v1.0/stations")
def Stations():
    """Redirected to the Station Page"""
    
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    # Query all stations
    no_stations=session.query(Station.name).all()

    session.close()

    # Convert list of tuples into normal list
    all_stations = list(np.ravel(no_stations))

    return jsonify(all_stations)
    
if __name__ == '__main__':
    app.run(debug=True)