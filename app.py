import numpy as np
import pandas as pd
from flask import Flask, jsonify
from sqlalchemy import create_engine, func, text
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

# Initialize Flask app
app = Flask(__name__)

# Set up SQLite connection
engine = create_engine("sqlite:///real_estate.sqlite")

# Reflect database table into a new model
Base = automap_base()
Base.prepare(engine)

# Save reference to the table
RealEstate = Base.classes.real_estate

# Helper function to execute raw SQL queries
def execute_query(query):
    with engine.connect() as conn:
        result = conn.execute(text(query))
        return [dict(row) for row in result.mappings()]
    
#################################################
# Flask Routes
#################################################

# Landing page
@app.route("/")
def welcome():
    return (
        f"<b>Welcome to the Real Estate API!</b><br/><br/>"
        f"Use the API endpoints below to query real estate data. Or don't. It's your life.<br/>"
        f"---------------------------------------------------------------------------------------------<br/>"
        f"<b>1. Get ALL Property Data:</b><br/>"
        f"/api/real_estate<br/><br/>"

        f"<b>2. Get a Property by ID:</b><br/>"
        f"/api/real_estate/&lt;id&gt;<br/><br/>"

        f"<b>3. Filter Properties by City:</b><br/>"
        f"/api/real_estate/city/&lt;city_name&gt;<br/><br/>"

        f"<b>4. Filter Properties by Price Range:</b><br/>"
        f"/api/real_estate/price/&lt;min_price&gt;/&lt;max_price&gt;<br/><br/>"

        f"<b>5. Properties by Year Built:</b><br/>"
        f"/api/real_estate/yearbuilt<br/><br/>"

        f"<b>6. Property Counts by Zip Code:</b><br/>"
        f"/api/real_estate/zip<br/><br/>"

        f"<b>7. Average Price per City:</b><br/>"
        f"/api/real_estate/avg_price/city<br/><br/>"

        f"<b>8. Price vs. Living Area:</b><br/>"
        f"/api/real_estate/price_livingarea<br/><br/>"

        f"<b>9. Feature Analysis:</b><br/>"
        f"/api/real_estate/feature_distribution<br/><br/>"

        f"<b>10. Property Type Distribution:</b><br/>"
        f"/api/real_estate/property_type_distribution<br/><br/>"

        f"<b>11. Map Visualization:</b><br/>"
        f"/api/real_estate/map<br/><br/>"
    )

# ORM routes
# Route 1: Get all property data (THIS IS SLOW! AVOID USING THIS IF POSSIBLE IT'S JUST FOR TESTING)
@app.route("/api/real_estate")
def get_all_properties():
    session = Session(engine)
    results = session.query(RealEstate).all()
    session.close()

    properties = []
    for result in results:
        property_dict = {
            "id": result.id,
            "datePostedString": result.datePostedString,
            "price": result.price,
            "pricePerSquareFoot": result.pricePerSquareFoot,
            "bedrooms": result.bedrooms,
            "bathrooms": result.bathrooms,
            "streetAddress": result.streetAddress,
            "city": result.city,
            "zipcode": result.zipcode,
            "latitude": result.latitude,
            "longitude": result.longitude,
            "yearBuilt": result.yearBuilt,
            "livingArea": result.livingArea,
            "parking": result.parking,
            "garageSpaces": result.garageSpaces,
            "pool": result.pool,
            "spa": result.spa,
            "isNewConstruction": result.isNewConstruction,
            "hasPetsAllowed": result.hasPetsAllowed,
            "homeType": result.homeType,
            "county": result.county,
            "event": result.event
        }
        properties.append(property_dict)

    return jsonify(properties)

# Route 2: Get a property by ID
@app.route("/api/real_estate/<id>")
def get_property_by_id(id):
    session = Session(engine)
    result = session.query(RealEstate).filter(RealEstate.id == id).first()
    session.close()

    if result:
        property_dict = {
            "id": result.id,
            "datePostedString": result.datePostedString,
            "price": result.price,
            "pricePerSquareFoot": result.pricePerSquareFoot,
            "bedrooms": result.bedrooms,
            "bathrooms": result.bathrooms,
            "streetAddress": result.streetAddress,
            "city": result.city,
            "zipcode": result.zipcode,
            "latitude": result.latitude,
            "longitude": result.longitude,
            "yearBuilt": result.yearBuilt,
            "livingArea": result.livingArea,
            "parking": result.parking,
            "garageSpaces": result.garageSpaces,
            "pool": result.pool,
            "spa": result.spa,
            "isNewConstruction": result.isNewConstruction,
            "hasPetsAllowed": result.hasPetsAllowed,
            "homeType": result.homeType,
            "county": result.county,
            "event": result.event
        }
        return jsonify(property_dict)
    else:
        return jsonify({"error": f"Property with ID {id} not found."}), 404

# Route 3: Filter properties by city
@app.route("/api/real_estate/city/<city_name>")
def filter_properties_by_city(city_name):
    session = Session(engine)
    results = session.query(RealEstate).filter(RealEstate.city == city_name).all()
    session.close()

    properties = []
    for result in results:
        property_dict = {
            "id": result.id,
            "datePostedString": result.datePostedString,
            "price": result.price,
            "pricePerSquareFoot": result.pricePerSquareFoot,
            "bedrooms": result.bedrooms,
            "bathrooms": result.bathrooms,
            "streetAddress": result.streetAddress,
            "city": result.city,
            "zipcode": result.zipcode,
            "latitude": result.latitude,
            "longitude": result.longitude,
            "yearBuilt": result.yearBuilt,
            "livingArea": result.livingArea,
            "parking": result.parking,
            "garageSpaces": result.garageSpaces,
            "pool": result.pool,
            "spa": result.spa,
            "isNewConstruction": result.isNewConstruction,
            "hasPetsAllowed": result.hasPetsAllowed,
            "homeType": result.homeType,
            "county": result.county,
            "event": result.event
        }
        properties.append(property_dict)

    return jsonify(properties)

# Route 4: Filter properties by price range
@app.route("/api/real_estate/price/<min_price>/<max_price>")
def filter_properties_by_price(min_price, max_price):
    session = Session(engine)
    results = session.query(RealEstate).filter(RealEstate.price.between(min_price, max_price)).all()
    session.close()

    properties = []
    for result in results:
        property_dict = {
            "id": result.id,
            "datePostedString": result.datePostedString,
            "price": result.price,
            "pricePerSquareFoot": result.pricePerSquareFoot,
            "bedrooms": result.bedrooms,
            "bathrooms": result.bathrooms,
            "streetAddress": result.streetAddress,
            "city": result.city,
            "zipcode": result.zipcode,
            "latitude": result.latitude,
            "longitude": result.longitude,
            "yearBuilt": result.yearBuilt,
            "livingArea": result.livingArea,
            "parking": result.parking,
            "garageSpaces": result.garageSpaces,
            "pool": result.pool,
            "spa": result.spa,
            "isNewConstruction": result.isNewConstruction,
            "hasPetsAllowed": result.hasPetsAllowed,
            "homeType": result.homeType,
            "county": result.county,
            "event": result.event
        }
        properties.append(property_dict)

    return jsonify(properties)

# Route 5: Properties by year built
@app.route("/api/real_estate/yearbuilt")
def yearbuilt_distribution():
    query = "SELECT yearBuilt, COUNT(*) AS propertyCount FROM real_estate GROUP BY yearBuilt"
    results = execute_query(query)
    return jsonify(results)

# Raw SQL routes
# Route 6: Property counts by zip code
@app.route("/api/real_estate/zip")
def zip_distribution():
    query = "SELECT zipcode, COUNT(*) AS propertyCount FROM real_estate GROUP BY zipcode"
    results = execute_query(query)
    return jsonify(results)

# Route 7: Average price per city
@app.route("/api/real_estate/avg_price/city")
def avg_price_by_city():
    query = "SELECT city, AVG(price) AS avgPrice FROM real_estate GROUP BY city"
    results = execute_query(query)
    return jsonify(results)

# Route 8: Price vs. living area
@app.route("/api/real_estate/price_livingarea")
def price_livingarea():
    query = "SELECT price, livingArea FROM real_estate"
    results = execute_query(query)
    return jsonify(results)

# Route 9: Feature analysis
@app.route("/api/real_estate/feature_distribution")
def feature_distribution():
    query = "SELECT pool, spa, isNewConstruction, hasPetsAllowed, COUNT(*) AS propertyCount FROM real_estate GROUP BY pool, spa, isNewConstruction, hasPetsAllowed"
    results = execute_query(query)
    return jsonify(results)

# Route 10: Property locations and some bonus info specifically for map visualization
@app.route("/api/real_estate/property_type_distribution")
def property_type_distribution():
    query = """
    SELECT homeType, COUNT(*) AS count
    FROM real_estate
    GROUP BY homeType
    """
    results = execute_query(query)
    return jsonify(results)

# Route 11: Property locations and some bonus info specifically for map visualization
@app.route("/api/real_estate/map")
def property_map():
    query = """
    SELECT city, zipcode, price, bedrooms, bathrooms, yearBuilt, livingArea, pool, homeType
    FROM real_estate
    """
    results = execute_query(query)
    return jsonify(results)

# Test URLs for routes with variable inputs (Copy & paste into your browser after running the app):

# Route 2: Get a property by ID
# http://127.0.0.1:5000/api/real_estate/7

# Route 3: Filter properties by city
# http://127.0.0.1:5000/api/real_estate/city/Los%20Angeles

# Route 4: Filter properties by price range
# http://127.0.0.1:5000/api/real_estate/price/3000000/5000000

if __name__ == '__main__':
    app.run(debug=True)

