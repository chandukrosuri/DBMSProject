function navigateToPage(pageName) {
    // Set the action attribute of the form to the Flask route
    console.log(pageName);
    var url = '/' + pageName;
    window
}

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
    const ctx = document.getElementById('myChart');

    new Chart(ctx, {
        type: 'line',  // Change the type to 'line'
        data: {
            labels: data.map(item => item.year),
            datasets: [{
                label: 'ratio',
                data: data.map(item => item.ratio),
                borderWidth: 1,
                borderColor: 'rgba(0, 0, 192, 1)',  // You can set the line color
                backgroundColor: 'rgba(75, 192, 192, 0.2)',  // You can set the fill color
            }]
        },
        options: {
            scales: {
                x: {
                    type: 'linear',
                    position: 'bottom'
                },
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}


$(document).ready(function() {
    // Event listener for form submission
    $('#submit-query-type').on('click', function(event) {
        event.preventDefault();
        var queryTypes = [].slice.call(document.getElementById('query-type'));
        var selctedType = queryTypes.filter(child => {return child.selected;})[0].value;

        if(selctedType === "default"){
            alert("Please select a card type");
        } else {
            getQueryPage(selctedType);
        }
    })
});

function getQueryPage(queryType){
    console.log("here");
    $.ajax({
        url: '/query-page',
        method: 'POST',
        data: queryType,
        processData: false,
        contentType: false,
        success: function(response) {
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