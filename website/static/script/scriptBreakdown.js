document.addEventListener('DOMContentLoaded', function () {
    var graphData = JSON.parse(document.getElementById('graph-data').textContent);

    var emissionFactorLabels = graphData[0];
    var emissionFactorValues = graphData[1];
    var dateLabels = graphData[2];
    var footprintValues = graphData[3];

    // Sample data for the average carbon footprint line (replace with actual data)
    var averageFootprintData = Array(dateLabels.length).fill(6500); // Assuming the average footprint is 50 units

    var pieCtx = document.getElementById('pie-chart').getContext('2d');
    var lineCtx = document.getElementById('line-chart').getContext('2d');

    var pieChart = new Chart(pieCtx, {
        type: 'pie',
        data: {
            labels: emissionFactorLabels,
            datasets: [{
                label: 'Emission Factors',
                data: emissionFactorValues,
                backgroundColor: [
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(255, 206, 86, 0.2)',
                    'rgba(75, 192, 192, 0.2)',
                    'rgba(153, 102, 255, 0.2)',
                    'rgba(255, 159, 64, 0.2)',
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(255, 206, 86, 0.2)',
                    'rgba(75, 192, 192, 0.2)'
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)',
                    'rgba(255, 159, 64, 1)',
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    position: 'right'
                }
            },
            title: {
                display: false,
                text: 'Footprint breakdown of monthly footprint by emission category' // Title for the pie chart
            }
        }
    });

    var lineChart = new Chart(lineCtx, {
        type: 'line',
        data: {
          labels: dateLabels.reverse(),
          datasets: [{
              label: 'Footprint',
              data: footprintValues.reverse(),
              backgroundColor: 'rgba(50, 210, 70, 0.6)',
              borderColor: 'rgba(0, 100, 0, 1.0)',
              borderWidth: 1
            },
            {
                label: 'UK Average',
                data: averageFootprintData,
                backgroundColor: 'rgba(255, 10, 10, 1)',
                borderColor: 'rgba(145, 10, 10, 1)',
                borderWidth: 1,
                fill: false,
                borderDash: [5, 5] // Dashed line style
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    }
                }]
            },
            plugins: {
                legend: {
                    position: 'right'
                }
            },
            title: {
                display: false,
                text: 'Carbon Footprint Progress' // Title for the line chart
            }
        }
    });
    //format improvements using regex-> makes the appearance sleeker
    var improvementsElement = document.querySelector('.text-container p');
    if (improvementsElement) {
        var formattedText = improvementsElement.innerHTML.replace(/(\d+\.\s\*\*)/g, '<br><br>$1');
        improvementsElement.innerHTML = formattedText;
    }
});
