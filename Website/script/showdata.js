'use strict';

let mycolors = ['#FFBD26', '#E04B3F', '#bcd4ff', '#5393ff'];
let ctxUptimeChart = document.getElementById('upTimeChart').getContext('2d');
let uptimeChart = new Chart(ctxUptimeChart, {
    type: 'bar',
    data: {
        labels: [],
        datasets: []
    },
    options: {
        defaultFontFamily: Chart.defaults.global.defaultFontFamily = "'Poppins'",
        maintainAspectRatio: false,
        title: {
            display: true,
            text: 'UP-Time',
            fontSize: 16,
            fontColor: '#242424'
        },
        scales: {
            yAxes: [{
                ticks: {
                    beginAtZero: true,
                    max: 24,
                    callback: function (value, index, values) {
                        return value + "h";
                    }
                }
            }]
        },
        tooltips: {
            mode: 'index',
            intersect: false,
            callbacks: {
                label: function (tooltipItem, data) {
                    if (tooltipItem.datasetIndex === 0) {
                        return `Raspberry was ${tooltipItem.value} hours online`;
                    } else if (tooltipItem.datasetIndex === 1) {
                        return `AP was ${tooltipItem.value} hours online`;
                    }
                }
            }
        }
    }
});


let ctxAccessCounterChart = document.getElementById('accessCounterChart').getContext('2d');
let accessCounterChart = new Chart(ctxAccessCounterChart, {
    type: 'line',
    data: {
        labels: [],
        datasets: []
    },
    options: {
        defaultFontFamily: Chart.defaults.global.defaultFontFamily = "'Poppins'",
        maintainAspectRatio: false,
        title: {
            display: true,
            text: 'Accesses',
            fontSize: 16,
            fontColor: '#242424'
        },
        tooltips: {
            mode: 'index',
            intersect: false,
            callbacks: {
                label: function (tooltipItem, data) {
                    return `The site was accessed ${tooltipItem.value} times`;
                }
            }
        },
        scales: {
            yAxes: [{
                ticks: {
                    callback: function (value, index, values) {
                        if (index % 2 === 0) {
                            return value;
                        } else {
                            return null;
                        }
                    }
                }
            }]
        },
    }
});


function updateCharts() {
    let xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            let data = JSON.parse(this.responseText);

            if (uptimeChart.data.datasets.length <= 0) {
                let raspberryUptime = {
                    label: 'Raspberry',
                    data: data.data.map(x => x.raspberryUptime),
                    backgroundColor: mycolors[0],
                    borderWidth: 0,
                    maxBarThickness: 20
                };
                let apUptime = {
                    label: 'Accesspoint',
                    data: data.data.map(x => x.apUptime),
                    backgroundColor: mycolors[1],
                    borderWidth: 0,
                    maxBarThickness: 20
                };
                uptimeChart.data.labels = data.data.map(x => x.date);
                uptimeChart.data.datasets.push(raspberryUptime, apUptime);
                uptimeChart.update();
            } else {
                uptimeChart.data.labels = data.data.map(x => x.date);
                uptimeChart.data.datasets[0].data = data.data.map(x => x.raspberryUptime);
                uptimeChart.data.datasets[1].data = data.data.map(x => x.apUptime);
                uptimeChart.update();
            }

            if (accessCounterChart.data.datasets.length <= 0) {
                let dailyAccesses = {
                    borderColor: mycolors[2],
                    data: data.data.map(x => x.accesses),
                    fill: false,
                    label: 'Accesses',
                    pointBackgroundColor: mycolors[3],
                    pointBorderColor: mycolors[3],
                    pointRadius: 3.5
                };
                accessCounterChart.data.labels = data.data.map(x => x.date);
                accessCounterChart.data.datasets.push(dailyAccesses);
                accessCounterChart.update();
            } else {
                accessCounterChart.data.labels = data.data.map(x => x.date);
                accessCounterChart.data.datasets[0].data = data.data.map(x => x.accesses);
                accessCounterChart.update();
            }
        }
    }

    xhttp.open("POST", "../Website/getChartData.php", true);
    xhttp.send();
}