function navigateToPage(pageName) {
    // Set the action attribute of the form to the Flask route
    console.log(pageName);
    var url = '/' + pageName;
    window.location.href = url;
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

$(document).ready(function() {
    // Event listener for form submission
    $('#submitForm').on('click', function(event) {
        event.preventDefault();
        var form = document.getElementById('q1Form');
        var formData = new FormData(form);
        console.log("formDate: ", formData);

        $.ajax({
            url: '/Q1',
            method: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            success: function(response) {
                // Handle the response here
                console.log('Data received:', response);
                console.log("res:", JSON.stringify(response.result));
                $("#result-container").removeClass("d-none");
                updateChart(response.result)
            },
            error: (functionError => {
                console.log(functionError);
            })
        });
    })
});

function updateChart(data) {
    console.log("response data: ", data);
    const ctx = document.getElementById('myChart');

    new Chart(ctx, {
        type: 'bar',
        data: {
        labels: data.map(function(item) { return item["name"]; }),
        datasets: [{
            label: '# of Votes',
            data: [12, 19, 3, 5, 2, 3],
            borderWidth: 1
        }]
        },
        options: {
        scales: {
            y: {
            beginAtZero: true
            }
        }
        }
    });
}