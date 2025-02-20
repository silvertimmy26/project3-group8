// Set initial map view to center of the USA
const map = L.map('map').setView([36.7783, -119.4179], 6);

// Add OpenStreetMap tiles to the map
let street = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

let topo = L.tileLayer('https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png', {
    attribution: 'Map data: &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, <a href="http://viewfinderpanoramas.org">SRTM</a> | Map style: &copy; <a href="https://opentopomap.org">OpenTopoMap</a> (<a href="https://creativecommons.org/licenses/by-sa/3.0/">CC-BY-SA</a>)'
});

// Clustering property markers for better performance
const markers = L.markerClusterGroup();
let layerControl; // Variable to store the layer control

function fetchData(city = '', minPrice = '', maxPrice = '', homeType = '', minYear = '', maxYear = '') {
    let url = `/api/real_estate/map?city=${city}&min_price=${minPrice}&max_price=${maxPrice}&home_type=${homeType}&min_year=${minYear}&max_year=${maxYear}`;

    fetch(url)
        .then(response => response.json())
        .then(data => {
            const heatArray = [];
            markers.clearLayers(); // Clear existing markers

            data.forEach(d => {
                const formattedPrice = '$' + d.price.toLocaleString();
                const marker = L.marker([d.latitude, d.longitude])
                    .bindPopup(`
                        <h5>City: ${d.city}</h5>
                        <h5>Price: ${formattedPrice}</h5>
                        <h5>Bedrooms: ${d.bedrooms}</h5>
                        <h5>Bathrooms: ${d.bathrooms}</h5>
                        <h5>Year Built: ${d.yearBuilt}</h5>
                        <h5>Home Type: ${d.homeType}</h5>`);
                markers.addLayer(marker);
                heatArray.push([d.latitude, d.longitude]);
            });

            map.addLayer(markers);

            // Create Heatmap Layer
            const heatLayer = L.heatLayer(heatArray, {
                radius: 25,
                blur: 10
            });

            // Add Cities Overlay
            const queryUrl = "https://raw.githubusercontent.com/codeforgermany/click_that_hood/refs/heads/main/public/data/california-counties.geojson";
            fetch(queryUrl)
                .then(response => response.json())
                .then(cityData => {
                    const mapStyle = {
                        color: "white",
                        fillColor: "green",
                        fillOpacity: 0.3,
                        weight: 1.5
                    };

                    const citiesLayer = L.geoJson(cityData, {
                        style: mapStyle,
                        onEachFeature: function (feature, layer) {
                            layer.bindPopup(feature.properties.city);
                        }
                    });

                    // Create the Layer Control
                    const baseMaps = {
                        Street: street,
                        Topography: topo,
                    };

                    const overlayMaps = {
                        HeatMap: heatLayer,
                        Listings: markers,
                        Cities: citiesLayer
                    };

                    // Add the Layer Control if it doesn't already exist
                    if (!layerControl) {
                        layerControl = L.control.layers(baseMaps, overlayMaps, {
                            collapsed: false
                        }).addTo(map);
                    }
                });
        })
        .catch(error => console.error('Error fetching data:', error));
}

function applyFilters() {
    const city = document.getElementById('city-filter').value;
    const minPrice = document.getElementById('min-price-filter').value;
    const maxPrice = document.getElementById('max-price-filter').value;
    const homeType = document.getElementById('home-type-filter').value.toUpperCase();
    const minYear = document.getElementById('min-year-filter').value;
    const maxYear = document.getElementById('max-year-filter').value;
    fetchData(city, minPrice, maxPrice, homeType, minYear, maxYear);
}

// Initial data fetch
fetchData();
