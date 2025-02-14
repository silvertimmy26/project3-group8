
  
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
    // For docs, refer to https://dev.socrata.com/docs/queries/where.html.
    // And, refer to https://dev.socrata.com/foundry/data.cityofnewyork.us/erm2-nwe9.
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
          <h3>${formattedPrice}</h3>
          <h3>${row.homeType}</h3>
          <h3>Bedrooms: ${row.bedrooms}</h3>
          <h3>Bathrooms: ${row.bathrooms}</h3>
          <h3>${row.city}</h3>`);
        markers.addLayer(marker);

          heatArray.push([row.latitude, row.longitude]);
      }
  
      // Create Heatmap Layer
      let heatLayer = L.heatLayer(heatArray, {
        radius: 25,
        blur: 10
      });

  
        // Step 3: CREATE THE LAYER CONTROL
        let baseMaps = {
          Street: street,
          Topography: topo
        };
  
        let overlayMaps = {
          HeatMap: heatLayer,
          Listings: markers
        };
  
        overlayMaps[complaint_type] = markers; // dynamic layer control key
  
        // Step 4: INITIALIZE THE MAP
        let myMap = L.map("map", {
          center: [36.7783, -119.4179],
          zoom: 6,
          layers: [street, markers]
        });
  
        // Step 5: Add the Layer Control, Legend, Annotations as needed
        L.control.layers(baseMaps, overlayMaps).addTo(myMap);
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
  