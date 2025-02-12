import numpy as np
import pandas as pd
from flask import Flask, jsonify
from sqlalchemy import create_engine, func
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

# Initialize Flask app
app = Flask(__name__)

# Set up SQLite connection
engine = create_engine("sqlite:///real_estate.sqlite")

# Reflect database table into a new model
Base = automap_base()
Base.prepare(engine, reflect=True)

# Save reference to the table
RealEstate = Base.classes.real_estate

# Helper function to execute raw SQL queries
def execute_query(query):
    with engine.connect() as conn:
        result = conn.execute(query)
        return [dict(row) for row in result]
    
#################################################
# Flask Routes
#################################################

def welcome():
    return (
        f"**Welcome to the Real Estate API!**<br/><br/>"
        f"Use the API endpoints below to query real estate data:<br/>"
        f"------------------------------------------------------<br/>"
        f"**1. Get All Properties:**<br/>"
        f"/api/v1.0/real_estate<br/><br/>"

        f"**2. Get a Property by ID:**<br/>"
        f"/api/v1.0/real_estate/&lt;id&gt;<br/><br/>"

        f"**3. Filter Properties by City:**<br/>"
        f"/api/v1.0/real_estate/city/&lt;city_name&gt;<br/><br/>"

        f"**4. Filter Properties by Price Range:**<br/>"
        f"/api/v1.0/real_estate/price/&lt;min_price&gt;/&lt;max_price&gt;<br/><br/>"

        f"**5. Properties by Year Built (Distribution):**<br/>"
        f"/api/v1.0/real_estate/yearbuilt_distribution<br/><br/>"

        f"**6. Property Counts by Zip Code (Heatmap):**<br/>"
        f"/api/v1.0/real_estate/zip_distribution<br/><br/>"

        f"**7. Average Price per City (Bar Chart):**<br/>"
        f"/api/v1.0/real_estate/avg_price/city<br/><br/>"

        f"**8. Price vs. Living Area (Scatter Plot):**<br/>"
        f"/api/v1.0/real_estate/price_livingarea<br/><br/>"

        f"**9. Feature Analysis (Venn Diagram):**<br/>"
        f"/api/v1.0/real_estate/feature_distribution<br/><br/>"

        f"**10. Property Locations for Map Visualization:**<br/>"
        f"/api/v1.0/real_estate/coordinates<br/><br/>"
    )
