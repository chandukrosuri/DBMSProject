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
                console.log(response.type);
                console.log("res:", JSON.stringify(response.result));
                $("#result-container").removeClass("d-none");
                updateChart(response)
            },
            error: (functionError => {
                console.log(functionError);
            })
        });
    })
});

function updateChart(data) {
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
                        text: 'Year',
                    },
                },
                y: {
                    min: Math.min(...data.map(item => item.ratio)),
                    title: {
                        display: true,
                        text: 'Ratio',
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