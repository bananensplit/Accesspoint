'use strict';
let mycolors = ['#f1544f', '#fa9242', 'rgba(44,139,219,0.3)', '#207dca'];

let ctxUptimeChart = document.getElementById('upTimeChart').getContext('2d');
let uptimeChart = new Chart(ctxUptimeChart, {
    type: 'bar',
    data: {
        datasets: []
    },
    options: {
        defaultFontFamily: Chart.defaults.global.defaultFontFamily = "'Poppins', sans-serif",
        maintainAspectRatio: false,
        title: {
            display: true,
            text: 'UP-Time',
            fontSize: 16,
            fontColor: '#242424'
        },
        scales: {
            xAxes: [{
                type: 'time',
                offset: true,
                distribution: 'series',
                time: {
                    minUnit: 'day',
                    unit: 'day'
                }
            }],
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
                        return `${data.datasets[0].label} - ${tooltipItem.value} up hours`;
                    } else if (tooltipItem.datasetIndex === 1) {
                        return `${data.datasets[1].label} - ${tooltipItem.value} up hours`;
                    }
                },
                title: function (tooltipItem, data) {
                    return moment(tooltipItem[0].label).format('DD.MMMM YYYY')
                }
            }
        }
    }
});


let ctxAccessCounterChart = document.getElementById('accessCounterChart').getContext('2d');
let accessCounterChart = new Chart(ctxAccessCounterChart, {
    type: 'line',
    data: {
        datasets: []
    },
    options: {
        defaultFontFamily: Chart.defaults.global.defaultFontFamily = "'Poppins', sans-serif",
        maintainAspectRatio: false,
        title: {
            display: true,
            text: 'Accesses',
            fontSize: 16,
            fontColor: '#242424'
        },
        legend: {
            display: false
        },
        scales: {
            xAxes: [{
                type: 'time',
                distribution: 'series',
                time: {
                    minUnit: 'day',
                    unit: 'day'
                },
            }],
            yAxes: [{
                ticks: {
                    beginAtZero: true,
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
        tooltips: {
            mode: 'index',
            intersect: false,
            callbacks: {
                label: function (tooltipItem, data) {
                    return `Site was accessed ${tooltipItem.value} times`;
                },
                title: function (tooltipItem, data) {
                    return moment(tooltipItem[0].label).format('DD.MMMM YYYY')
                }
            }
        }
    }
});

function updateCharts(dataAmount = 100) {
    if (dataAmount < 14) dataAmount = 14;

    let xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            let data = JSON.parse(this.responseText);

            if (uptimeChart.data.datasets.length <= 0) {
                let raspberryUptime = {
                    label: 'Raspberry',
                    data: data.data
                        .filter((value, index) => index < dataAmount)
                        .map(x => ({x: x.date, y: secToHourAndRound(x.raspberryUptime)})),
                    backgroundColor: mycolors[0],
                };
                let apUptime = {
                    label: 'Accesspoint',
                    data: data.data
                        .filter((value, index) => index < dataAmount)
                        .map(x => ({x: x.date, y: secToHourAndRound(x.apUptime)})),
                    backgroundColor: mycolors[1],
                };
                uptimeChart.data.datasets.push(raspberryUptime, apUptime);
                uptimeChart.update();
            } else {
                uptimeChart.data.datasets[0].data = data.data
                    .filter((value, index) => index < dataAmount)
                    .map(x => ({x: x.date, y: secToHourAndRound(x.raspberryUptime)}));
                uptimeChart.data.datasets[1].data = data.data
                    .filter((value, index) => index < dataAmount)
                    .map(x => ({x: x.date, y: secToHourAndRound(x.apUptime)}));
                uptimeChart.update();
            }

            if (accessCounterChart.data.datasets.length <= 0) {
                let dailyAccesses = {
                    label: 'Accesses',
                    data: data.data
                        .filter((value, index) => index < dataAmount)
                        .map(x => ({x: x.date, y: x.accesses})),
                    borderColor: mycolors[3],
                    borderWidth: 2,
                    lineTension: 0,
                    backgroundColor: mycolors[2],
                    pointBackgroundColor: mycolors[3],
                    pointBorderColor: mycolors[3],
                    pointRadius: 0
                };
                accessCounterChart.data.datasets.push(dailyAccesses);
                accessCounterChart.update();
            } else {
                accessCounterChart.data.datasets[0].data = data.data
                    .filter((value, index) => index < dataAmount)
                    .map(x => ({x: x.date, y: x.accesses}));
                accessCounterChart.update();
            }
        }
    }

    xhttp.open("POST", "getChartData.php", true);
    xhttp.send();
}

function secToHourAndRound(seconds, decimals = 2) {
    decimals = Math.pow(10, decimals);
    let hours = seconds / 60 / 60;
    return Math.round(hours * decimals) / decimals;
}

updateCharts();