function navigateToPage(pageName) {
    // Set the action attribute of the form to the Flask route
    console.log(pageName);
    var url = '/query-page/' + pageName;
    window.location.href = url
}

$(function() {    
    $('option').on('click', function(event) {
        event.preventDefault();
        var value1 = $('#value1_q1').val();
        var value2 = $('#value2_q1').val();
        var value3 = $('#value3_q1').val();
        var form = document.getElementById("q1Form");
        var formName = form.name;
    })
});

function toggleDropdown() {
    var dropdownContent = document.getElementById("dropdownContent");
    dropdownContent.classList.toggle("show");
}

// function toggleResultDiv(pageName) {
//     var resultContainer = document.getElementById("result-container-" + pageName);
//     resultContainer.style.display = "block";
//     window.location.href = "/" + pageName;
// }
  // Event listener for form submission
$(function() {    
    $('#submitForm').on('click', function(event) {
        event.preventDefault();
        var value1 = $('#value1_q1').val();
        var value2 = $('#value2_q1').val();
        var value3 = $('#value3_q1').val();
        var form = document.getElementById("q1Form");
        var formName = form.name;


        // Do something with the values
        console.log('Value from the first select:', value1);
        console.log('Value from the second select:', value2);
        console.log('List of values from the third select:', value3);
        console.log('formName: ', formName);

        var formData = new FormData();
        formData.append('value1_q1', value1);
        formData.append('value2_q1', value2);
        formData.append('value3_q1', JSON.stringify(value3));
        formData.append("query_type", formName);

        $.ajax({
            url: '/query-data',
            method: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            success: function(response) {
                // Handle the response here
                console.log('Data received:', response);
                $("#result-container").removeClass("d-none");
                updateChart(response, formName);
                enableHeatMapFilters(formName);
            },
            error: (functionError => {
                console.log(functionError);
            })
        });
    })
});

function updateChart(data, queryType) {
    console.log("data: ", data);
    console.log("response data: ", data[0].ratio);
    const canvas = document.getElementById('myChart');

    // Check if a Chart instance already exists
    if (canvas.chart) {
        // Destroy the existing Chart instance
        canvas.chart.destroy();
    }

    const brightColors = ['#FF5733', '#33FF57', '#5733FF', '#FF336E', '#33A7FF'];
    const datasets = {};

    // Prepare datasets for different countries
    data.forEach(item => {
        if (!datasets[item.country]) {
            datasets[item.country] = {
                label: item.country,
                data: [],
                borderColor: brightColors.pop(),
                backgroundColor: 'rgba(0, 0, 0, 0)', // Set a transparent background
                borderWidth: 2,
                fill: false,
            };
        }
        datasets[item.country].data.push({ x: item.year, y: item.ratio });
    });

    // Create a new Chart instance
    const ctx = canvas.getContext('2d');
    var [xLabel, yLabel] = getLabels(queryType);
    canvas.chart = new Chart(ctx, {
        type: 'line',
        data: {
            datasets: Object.values(datasets),
        },
        options: {
            scales: {
                x: {
                    type: 'linear',
                    position: 'bottom',
                    ticks: {
                        callback: function (value) {
                            return Number.isInteger(value) ? value : '';
                        },
                    },
                    title: {
                        display: true,
                        text: xLabel,
                    },
                },
                y: {
                    min: Math.min(...data.map(item => item.ratio)),
                    title: {
                        display: true,
                        text: yLabel,
                    },
                },
            },
        },
    });
}



// Function to generate random colors
function getRandomColor() {
    const letters = '0123456789ABCDEF';
    let color = '#';
    for (let i = 0; i < 6; i++) {
        color += letters[Math.floor(Math.random() * 16)];
    }
    return color;
}



$(document).ready(function() {
    // Event listener for form submission
    $('#submit-query-type').on('click', function(event) {
        event.preventDefault();
        var queryTypes = [].slice.call(document.getElementById('query-type'));
        var selectedType = queryTypes.filter(child => {return child.selected;})[0].value;

        if(selectedType === "default"){
            alert("Please select a card type");
        } else {
            console.log(selectedType);
            console.log(selectedType.split("-"));
            var queryType = selectedType.split("-")[0];
            var pageNumber = selectedType.split("-")[1];
            getQueryPage(queryType, pageNumber);
        }
    })
});

function getQueryPage(queryType, pageNumber){
    console.log("here");
    $.ajax({
        url: ('/query-page').concat("/",pageNumber),
        method: 'POST',
        data: queryType,
        processData: false,
        contentType: false,
        success: function(response) {
            console.log(response);
            // Handle the response here
            $(".filters").removeClass("d-none");
            // updateChart(response.result)
            $("#selects").removeClass("d-none");
            var s = ''
            for (var i = 0; i < response["years"].length; i++) {  
                var value = response["years"][i];
                s += '<option value="' + value + '">' + value + '</option>';  
            }
            $("#value1_q1").append(s);

            var s = ''
            for (var i = 0; i < response["years"].length; i++) {  
                var value = response["years"][i];
                s += '<option value="' + value + '">' + value + '</option>'; 
            }
            $("#value2_q1").append(s);

            var s = ''
            for (var i = 0; i < response["final_country"].length; i++) {  
                var value = response["final_country"][i];
                s += '<option value="' + value + '">' + value + '</option>'; 
            }
            $("#value3_q1").append(s);
            
            $("#q1Form").attr("name", queryType);
        },
        error: (functionError => {
            console.log(functionError);
        })
    });
}

function enableHeatMapFilters(queryType){
    $("#year-filter").removeClass("d-none");
    $("#map-filter").removeClass("d-none");
    console.log("enableHeatMapFilters: ", queryType);
    $.ajax({
        url: ('/years').concat("/",queryType),
        method: 'GET',
        processData: false,
        contentType: false,
        success: function(response){
            console.log("heatmap: ",response['years']);
            var s = '';
            for (var i = 0; i < response["years"].length; i++) {  
                var value = response["years"][i];
                s += '<option value="' + value + '">' + value + '</option>';  
            }
            $("#map-year").append(s);
            $("#map-year").attr("name", queryType);
        },
        error: (functionError => {
            console.log(functionError);
        })
    })
}

$(function() {    
    $('#generate').on('click', function(event) {
        event.preventDefault();
        var value1 = $('#map-year').val();
        var form = document.getElementById("q1Form");
        var formName = form.name;
        initializeMap(formName, value1);
    });
});

function getLabels(queryType) {
    switch (queryType) {
        case 'education_gdp_ratio':
            return ['Year', 'GDP (scaled to 100,000,000)/Avg_Years_Of_Education Ratio'];

        case 'debt_expen_ratio':
            return ['Year', 'Debt/Expenditure Ratio'];

        case 'happiness_change':
            return ['Year', 'Happiness Percentage Change'];

        case 'obesity_change':
            return ['Year', 'Obesity Percentage Change'];

        case 'suicide_mean':
            return ['Year', 'Suicide Rate Mean Deviation'];

        case 'pollution_rank':
            return ['Year', 'Air Pollution Rank'];

        case 'medical_contribution':
            return ['Year', 'Percentage of Global Medical Personnel'];

        default:
            // Default labels if queryType doesn't match any case
            return ['X Label', 'Y Label'];
    }
}

function getColorForDataValue(dataValue, maxValue) {
    // Use a logarithmic scale for a better color spread
    const minHue = 240; // blue color
    const maxHue = 0; // red color
    const logValue = Math.log(dataValue + 1); // adding 1 to avoid log(0)
    const logMax = Math.log(maxValue + 1); // adding 1 to avoid log(0)
    const scale = (logValue / logMax);
    const hue = minHue + scale * (maxHue - minHue);
    return `hsl(${hue}, 100%, 50%)`;
}


function initializeMap(queryType, year) {
    console.log("here initializeMap")
    $("#map").removeClass("d-none");
    var map = L.map('map').setView([20, 0], 2); // World view
    // Fetch the max data value first
    fetch('/api/max_value?'+ new URLSearchParams({
        'queryType': queryType,
        'year': year,
    }))

    .then(response => response.json())
    .then(response => {
        const maxValue = response.max_value;
        console.log(maxValue)
        // Then fetch the actual data
        fetch('/api/data?' + new URLSearchParams({
            'queryType': queryType,
            'year': year,
        }))
        .then(response => response.json())
        .then(arrayData => {
            const data = arrayData.reduce((obj, item) => {
                obj[item.country] = item.ratio;
                return obj;
            }, {});
            // console.log("Processed data object:", data);
            fetch('/static/countries.geo.json')
            .then(response => response.json())
            .then(geojsonData => {
                // Add the GeoJSON layer
                L.geoJson(geojsonData, {
                    style: function(feature) {
                        var countryName = feature.properties.name;
                        var dataValue = data[countryName] || 0;
                        var fillColor = getColorForDataValue(dataValue, maxValue);
                        // console.log(`Styling ${countryName}: Data Value = ${dataValue}, Color = ${fillColor}`);
                        // console.log(`Styling ${countryName}: Data Value = ${dataValue}`);
                        return {
                            fillColor: fillColor,
                            weight: 2,
                            opacity: 1,
                            color: 'white',
                            fillOpacity: 0.7
                        };
                    }
                }).addTo(map);
            });
        })
        .catch(error => console.error('Error fetching data:', error));
    });
}
