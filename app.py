import numpy as np
import pandas as pd
from flask import Flask, jsonify, render_template, request
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
def index():
    return render_template('index.html')

# ORM API routes
# Get all property data (THIS IS SLOW! AVOID USING THIS IF POSSIBLE IT'S JUST FOR TESTING)
@app.route("/api/real_estate")
def get_all_properties():
    session = Session(engine)
    results = session.query(RealEstate).all()
    session.close()

    properties = []
    for result in results:
        property_dict = {
            "id": result.id,
            "date": result.date,
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

# Get a property by ID
@app.route("/api/real_estate/<id>")
def get_property_by_id(id):
    session = Session(engine)
    result = session.query(RealEstate).filter(RealEstate.id == id).first()
    session.close()

    if result:
        property_dict = {
            "id": result.id,
            "date": result.date,
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

# Filter properties by city
@app.route("/api/real_estate/city/<city_name>")
def filter_properties_by_city(city_name):
    session = Session(engine)
    results = session.query(RealEstate).filter(RealEstate.city == city_name).all()
    session.close()

    properties = []
    for result in results:
        property_dict = {
            "id": result.id,
            "date": result.date,
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

# Filter properties by price range
@app.route("/api/real_estate/price/<min_price>/<max_price>")
def filter_properties_by_price(min_price, max_price):
    session = Session(engine)
    results = session.query(RealEstate).filter(RealEstate.price.between(min_price, max_price)).all()
    session.close()

    properties = []
    for result in results:
        property_dict = {
            "id": result.id,
            "date": result.date,
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

# Properties by year built
@app.route("/api/real_estate/yearbuilt")
def yearbuilt_distribution():
    query = "SELECT yearBuilt, COUNT(*) AS propertyCount FROM real_estate GROUP BY yearBuilt"
    results = execute_query(query)
    return jsonify(results)

# Raw SQL API routes
# Property counts by zip code
@app.route("/api/real_estate/zip")
def zip_distribution():
    query = "SELECT zipcode, COUNT(*) AS propertyCount FROM real_estate GROUP BY zipcode"
    results = execute_query(query)
    return jsonify(results)

# Average price per county
@app.route("/api/real_estate/avg_price_county")
def avg_price_by_county():
    query = """
    SELECT REPLACE(county, ' County', '') AS county, ROUND(AVG(price), 2) AS avgPrice
    FROM real_estate
    WHERE county IS NOT NULL
    GROUP BY county
    """
    results = execute_query(query)
    return jsonify(results)

# Feature analysis
@app.route("/api/real_estate/feature_distribution")
def feature_distribution():
    query = "SELECT pool, spa, isNewConstruction, hasPetsAllowed, COUNT(*) AS propertyCount FROM real_estate GROUP BY pool, spa, isNewConstruction, hasPetsAllowed"
    results = execute_query(query)
    return jsonify(results)

# Property locations and some bonus info specifically for map visualization
@app.route("/api/real_estate/property_type_distribution")
def property_type_distribution():
    query = """
    SELECT homeType, COUNT(*) AS count
    FROM real_estate
    GROUP BY homeType
    """
    results = execute_query(query)
    return jsonify(results)

# Property locations and some bonus info specifically for map visualization
@app.route("/api/real_estate/map")
def property_map():
    query = """
    SELECT city, price, bedrooms, bathrooms, yearBuilt, homeType, latitude, longitude
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

# Frontend visualizations
# TODO: add redirect to home page from visualizations
@app.route('/map')
def map():
    return render_template('map.html')

# REWORK THIS to data table, needed for plotly dashboard
@app.route('/scatter')
def scatter():
    return render_template('scatter.html')

@app.route('/choropleth_county')
def choropleth_county():
    return render_template('choropleth_county.html')

@app.route('/property_type_distribution')
def property_type_distribution_page():
    return render_template('property_type_distribution.html')

@app.route('/year_built')
def year_built():
    return render_template('year_built.html')

if __name__ == '__main__':
    app.run(debug=True)

