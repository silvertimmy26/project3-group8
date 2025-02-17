function createMap(complaint_type) {
  // Delete Map
  let map_container = d3.select("#map_container");
  map_container.html(""); // empties it
  map_container.append("div").attr("id", "map"); //recreate it
  
  
// Step 1: CREATE THE BASE LAYERS
let street = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
})

let topo = L.tileLayer('https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png', {
attribution: 'Map data: &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, <a href="http://viewfinderpanoramas.org">SRTM</a> | Map style: &copy; <a href="https://opentopomap.org">OpenTopoMap</a> (<a href="https://creativecommons.org/licenses/by-sa/3.0/">CC-BY-SA</a>)'
});

// Store the API query variables.
let baseURL = "https://data.ca.gov/api/3/action/datastore_search?resource_id=your_dataset_id";
// Add the dates in the ISO formats
let date = "$where=created_date between'2024-01-01T00:00:00' and '2025-01-01T00:00:00'";
// Add the complaint type.
let complaint = `&complaint_type=${complaint_type}`;
// Add a limit.
let limit = "&$limit=10000";

// Assemble the API query URL.
let url = "/api/real_estate/map";
console.log(url);

d3.json(url).then(function (data) {

  // Step 2: CREATE THE DATA/OVERLAY LAYERS
    console.log(data);

  // Initialize the Cluster Group
    let heatArray = [];
    let markers = L.markerClusterGroup();

  // Loop and create marker
    for (let i = 0; i < data.length; i++){
      let row = data[i];

    // Format markers 
      let formattedPrice = '$' + row.price.toLocaleString(); // Use toLocaleString to format with commas for thousands, if needed

    // Create the marker and bind the popup with the formatted price
        let marker = L.marker([row.latitude, row.longitude]).bindPopup(`
          <h5>${formattedPrice}</h5>
          <h5>Home Type: ${row.homeType}</h5>
          <h5>${row.bedrooms} Bedrooms</h5>
          <h5>${row.bathrooms} Bathrooms</h5><hr>
          <h5>${row.city}, CA</h5>`);
        markers.addLayer(marker);
        heatArray.push([row.latitude, row.longitude]);
      }

      // Create Heatmap Layer
      let heatLayer = L.heatLayer(heatArray, {
        radius: 25,
        blur: 10
      });

      // Add Cities Overlay 
      let queryUrl = "https://raw.githubusercontent.com/codeforgermany/click_that_hood/refs/heads/main/public/data/california-counties.geojson";
      d3.json(queryUrl).then(function(cityData) { 
        
        // Our style object
        let mapStyle = {
          color: "white",
          fillColor: "green",
          fillOpacity: 0.3,
          weight: 1.5
        };

        let citiesLayer = L.geoJson(cityData, {
          style: mapStyle,
          onEachFeature: function (feature, layer) {
            layer.bindPopup(feature.properties.city);
          }
        });


        // Step 3: CREATE THE LAYER CONTROL
          let baseMaps = {
            Street: street,
            Topography: topo,
          };

          let overlayMaps = {
            HeatMap: heatLayer,
            Listings: markers,
            Cities: citiesLayer
          };


        // Step 4: INITIALIZE THE MAP
          let myMap = L.map("map", {
            center: [36.7783, -119.4179],
            zoom: 6,
            layers: [street, markers, citiesLayer]
          });

        // Step 5: Add the Layer Control, Legend, Annotations as needed
          L.control.layers(baseMaps, overlayMaps, {
            collapsed: false
          }).addTo(myMap);
        });
      });
    }

function init() {
let complaint_type = d3.select("#complaint_type").property("value");
createMap(complaint_type);
}


// Event Listener
d3.select("#filter-btn").on("click", function () {
init();
});

// on page load
init();

  