<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="{{ url_for('static', filename='css/styleVisualise.css') }}">
    <title>Sign-up - Carbon Footprint Tracker</title>
</head>
<body>
  <div id="graph-data" style="display: none;">{{ graph_data | tojson }}</div>
  <div class="container">
      <div class="chart-container" id="pie-chart-container">
          <canvas id="pie-chart"></canvas>
      </div>
      <div class="chart-container" id="line-chart-container">
          <canvas id="line-chart"></canvas>
      </div>
  </div>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script src="{{ url_for('static', filename='script/scriptBreakdown.js') }}"></script>
</body>
</html>


document.addEventListener('DOMContentLoaded', function () {
    var graphData = JSON.parse(document.getElementById('graph-data').textContent);

    var emissionFactorLabels = graphData[0];
    var emissionFactorValues = graphData[1];
    var dateLabels = graphData[2];
    var footprintValues = graphData[3];

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
            responsive: true
        }
    });

    var lineChart = new Chart(lineCtx, {
        type: 'line',
        data: {
            labels: dateLabels,
            datasets: [{
                label: 'Carbon Footprint',
                data: footprintValues,
                backgroundColor: 'rgba(54, 162, 235, 0.2)',
                borderColor: 'rgba(54, 162, 235, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    }
                }]
            }
        }
    });
});
