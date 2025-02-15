from sqlalchemy import create_engine, text, func

import pandas as pd

# Define the SQLHelper Class
# PURPOSE: Deal with all of the database logic

class SQLHelper():

    # Initialize PARAMETERS/VARIABLES

    #################################################
    # Database Setup
    #################################################
    def __init__(self):
        self.engine = create_engine("sqlite:///real_estate.sqlite")

    #################################################################

    def queryMapData(self):
        # Create our session (link) from Python to the DB
        conn = self.engine.connect() # Raw SQL/Pandas

        # Define Query
        query = text("""SELECT
                    city,
                    zipcode,
                    price,
                    bedrooms,
                    isNewConstruction,
                    homeType,
                    latitude,
                    longitude
                FROM
                    real_estate
                ORDER BY
                    city asc;""")
        df = pd.read_sql(query, con=conn)

        # Close the connection
        conn.close()
        return(df)

    