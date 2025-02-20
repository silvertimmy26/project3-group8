# Real Estate Data Visualization Project

## Team Members
- Arya Maredia
- Asia Byrne
- Cecilia Rocha
- Josh Ehlke
- Matthew Adent

## Project Overview
This project provides data visualization for real estate data in California. The visualizations include interactive dashboards and APIs.. The visualizations are built using Plotly, ECharts, and Leaflet, and the backend is powered by Flask.

## File Structure

### Root Directory
- `README.md`: This file!
- `app.py`: The main Flask application file that sets up the backend API and routes.

### Data Processing
- `data_wrangling.ipynb`: A Jupyter Notebook that cleans and processes the real estate data, storing it in an SQLite database (`real_estate.sqlite`).
- `data/RealEstate_California.csv`: Our California real estate dataset in CSV format.

### Templates
- `templates/index.html`: The landing page of the application.
- `templates/map.html`: The HTML template for the map dashboard.
- `templates/dashboard.html`: The HTML template for the Plotly (and other libraries) dashboard.
- `templates/works_cited.html`: References for our project.
- `templates/about_us.html`: Gives some details about the team behind our project. Hey, that's us!

### Static Files
- `static/js/map.js`: JavaScript file for handling the map dashboard functionalities.
- `static/js/visualizations.js`: JavaScript file for handling the Plotly dashboard visualizations.
- `static/js/leaflet-heat.js`: Open source JavaScript library for creating heatmaps with Leaflet, not our creation. Credit listed at the top of the file.
- `static/images`: Photos of us for the 'About Us' section, and for the buttons on the landing page.

## License
This project is licensed under the MIT License.
