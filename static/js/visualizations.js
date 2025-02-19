function fetchData(city = '', homeType = '', year = '') {
    let url = `/api/real_estate/data?city=${city}&home_type=${homeType}&year=${year}`;

    // Property Type Distribution (Apache ECharts Pie Chart)
    fetch(`/api/real_estate/property_type_distribution?city=${city}&home_type=${homeType}&year=${year}`)
        .then(response => response.json())
        .then(data => {
            const chart = echarts.init(document.getElementById('property-type-chart'));
            const chartData = data.map(item => ({ name: item.homeType, value: item.count }));
            const option = {
                title: { text: 'Property Type Distribution', left: 'center' },
                tooltip: { trigger: 'item', formatter: '{a} <br/>{b}: {c} ({d}%)' },
                legend: { orient: 'vertical', left: 'left' },
                series: [{ name: 'Property Type', type: 'pie', radius: '50%', data: chartData }]
            };
            chart.setOption(option);
        });

    // Average Price by County Choropleth (Apache ECharts Choropleth)
    Promise.all([
        fetch(`/api/real_estate/avg_price_county?city=${city}&home_type=${homeType}&year=${year}`).then(res => res.json()),
        fetch('https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/california-counties.geojson').then(res => res.json())
    ])
    .then(([countyData, geoJson]) => {
        const chart = echarts.init(document.getElementById('choropleth-chart'));
        echarts.registerMap('california', geoJson);

        const dataMap = {};
        countyData.forEach(item => {
            dataMap[item.county] = item.avgPrice;
        });

        const formattedData = geoJson.features.map(feature => ({
            name: feature.properties.name,
            value: dataMap[feature.properties.name] || 0 // Fill 0 if no data
        }));

        chart.setOption({
            title: { text: 'Average Property Price by County', left: 'center' },
            tooltip: {
                trigger: 'item',
                formatter: params => `${params.name}: $${params.value.toLocaleString()}`
            },
            visualMap: {
                min: 0,
                max: 3000000, // Adjust depending on price range
                text: ['High', 'Low'],
                realtime: false,
                calculable: true,
                color: ['#00429d', '#97d4e9']
            },
            series: [{
                type: 'map',
                map: 'california',
                roam: true,
                label: { show: false },
                data: formattedData
            }]
        });
    })
    .catch(error => console.error('Error loading data:', error));

    // Year Built Distribution (Plotly Histogram)
    fetch(`/api/real_estate/yearbuilt?city=${city}&home_type=${homeType}`)
        .then(response => response.json())
        .then(data => {
            const years = [];
            // Intervals of 5 years from 1850 to 2025
            data.forEach(item => {
                for (let i = 0; i < item.propertyCount; i++) years.push(item.yearBuilt);
            });
            Plotly.newPlot('year-built-chart', [{
                x: years,
                type: 'histogram',
                histnorm: 'percent',
                opacity: 0.7,
                marker: {
                    color: 'rgba(100, 149, 237, 0.7)',
                    line: { color: 'black', width: 1 }
                },
                xbins: { size: 5 },
                hovertemplate: '%{x}, %{y:.2f}%<extra></extra>'
            }], { 
                title: 'Year Built Distribution', 
                xaxis: { title: { text: 'Year Built' }, tickformat: 'd', range: [1850, 2025], dtick: 10 }, 
                yaxis: { title: { text: 'Percentage of Houses' }, tickformat: '.2f', range: [0, 15] }, 
                bargap: 0.05
            });
        });

    // Data Table (DataTables data table)
    fetch(`/api/real_estate/data_table?city=${city}&home_type=${homeType}&year=${year}`)
        .then(response => response.json())
        .then(data => {
            // Destroy existing DataTable instance if it exists OR ELSE suffer the consequences
            if ($.fn.DataTable.isDataTable('#propertyTable')) {
                $('#propertyTable').DataTable().clear().destroy();
            }

            $('#propertyTable').DataTable({
                data: data,
                columns: [
                    { data: 'streetAddress' },
                    { data: 'city' },
                    { data: 'zipcode' },
                    { data: 'price' },
                    { data: 'bedrooms' },
                    { data: 'bathrooms' },
                    { data: 'livingArea' },
                    { data: 'yearBuilt' },
                    { data: 'homeType' }
                ],
                pageLength: 10
            });
        });
}

function applyFilters() {
    const city = document.getElementById('city-filter').value;
    const homeType = document.getElementById('home-type-filter').value.toUpperCase();
    const year = document.getElementById('year-filter').value;
    fetchData(city, homeType, year);
}

// Initial data fetch
fetchData();
