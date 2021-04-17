'use strict';
let mycolors = ['#f1544f', '#fa9242', 'rgba(44,139,219,0.3)', '#207dca'];

// Default Font-Family
Chart.defaults.font.family = "'Poppins', sans-serif";

// Default Title configurtion
Chart.defaults.plugins.title.display = true;
Chart.defaults.plugins.title.color = '#000000';
Chart.defaults.plugins.title.font = {
    weight: 'bold',
    size: 17,
};
Chart.defaults.plugins.title.padding = 3;

let ctxUptimeChart = document.getElementById('upTimeChart').getContext('2d');
let uptimeChart = new Chart(ctxUptimeChart, {
    type: 'bar',
    data: {
        datasets: [{
            label: "Raspberry",
            data: [],
            backgroundColor: mycolors[0],
            maxBarThickness: 10,
        }, {
            label: "Accesspoint",
            data: [],
            backgroundColor: mycolors[1],
            maxBarThickness: 10,
        }]
    },
    options: {
        maintainAspectRatio: false,
        responsive: true,
        interaction: {
            mode: 'x',
            intersect: false,
        },
        scales: {
            x: {
                type: 'time',
                time: {
                    minUnit: 'day',
                    unit: 'day'
                },
            },
            y: {
                min: 0,
                max: 24,
                ticks: {
                    callback: value => value + 'h'
                },
            }
        },
        plugins: {
            title: {
                text: 'UP-Time'
            },
            tooltip: {
                callbacks: {
                    label: function (context) {
                        if (context.datasetIndex === 0) {
                            if (context.raw.y.length === 0) {
                                return `Raspberry was not online`
                            }
                            return `Raspberry: ${hourToTime(context.raw.y[0])} - ${hourToTime(context.raw.y[1])}`
                        } else if (context.datasetIndex === 1) {
                            if (context.raw.y.length === 0) {
                                return `Accesspoint was not online`
                            }
                            return `Accesspoint: ${hourToTime(context.raw.y[0])} - ${hourToTime(context.raw.y[1])}`
                        }
                    },
                    title: (context) => moment(context[0].label).format('DD.MMMM YYYY')
                }
            }
        }
    }
});


let ctxAccessCounterChart = document.getElementById('accessCounterChart').getContext('2d');
let accessCounterChart = new Chart(ctxAccessCounterChart, {
    type: 'line',
    data: {
        datasets: [{
            label: 'Accesses',
            data: [],
            borderColor: mycolors[3],
            backgroundColor: mycolors[2],
            fill: true,
            pointRadius: 0
        }]
    },
    options: {
        maintainAspectRatio: false,
        responsive: true,
        interaction: {
            mode: 'index',
            intersect: false
        },
        scales: {
            x: {
                type: 'time',
                time: {
                    minUnit: 'day',
                    unit: 'day'
                },
            },
            y: {
                min: 0,
            }
        },
        plugins: {
            title: {
                text: 'Accesses'
            },
            tooltip: {
                mode: 'index',
                intersect: false,
                callbacks: {
                    label: (context) => `Site was accessed ${context.raw.y} times`,
                    // label: (context) => console.log(context.raw.y),
                    title: (context) => moment(context[0].label).format('DD.MMMM YYYY')
                }
            }
        },

    }
});


// let socket = new MyWebsocket('ws://127.0.0.1:3000')
let socketCharts = new MyWebsocket('ws://192.168.0.100:3000')

async function getData() {
    while (!socketCharts.checkIfUp()) {
        await sleep(1000)
    }
    socketCharts.getData('chartData').then(value => updateCharts(JSON.parse(value.data)))
}

function secToHourAndRound(seconds, decimals = 2) {
    decimals = Math.pow(10, decimals);
    let hours = seconds / 60 / 60;
    return Math.round(hours * decimals) / decimals;
}

function hourToTime(hours) {
    hours = hours === 24.0 ? 86399999 : (hours * 60 * 60 * 1000)
    return moment(hours).utc().format('HH:mm:ss');
}

function updateCharts(data) {
    console.log(data.data);

    let ergUptimeAP = []
    for (let i = 0; i < data.data.length; i += 1) {
        let element = data.data[i]

        if (element['ap-actions'].length === 0) {
            ergUptimeAP.push({x: element['date'], y: []})
        }

        for (let j = 0; j < element['ap-actions'].length; j += 2) {
            ergUptimeAP.push({
                x: element['date'],
                y: [secToHourAndRound(element['ap-actions'][j]['time']), secToHourAndRound(element['ap-actions'][j + 1]['time'])],
            })
        }
    }

    let ergUptimeRP = []
    for (let i = 0; i < data.data.length; i += 1) {
        let element = data.data[i]

        if (element['rp-actions'].length === 0) {
            ergUptimeRP.push({x: element['date'], y: []})
        }

        for (let j = 0; j < element['rp-actions'].length; j += 2) {
            ergUptimeRP.push({
                x: element['date'],
                y: [secToHourAndRound(element['rp-actions'][j]['time']), secToHourAndRound(element['rp-actions'][j + 1]['time'])],
            })
        }
    }

    ergUptimeRP.forEach((value, index) => uptimeChart.data.datasets[0].data[index] = value)
    ergUptimeAP.forEach((value, index) => uptimeChart.data.datasets[1].data[index] = value)
    uptimeChart.update();


    data.data.forEach((value, index) => accessCounterChart.data.datasets[0].data[index] = {
        x: value['date'],
        y: value['accesses']
    });
    accessCounterChart.update();
}

function sleep(milliseconds) {
    return new Promise(resolve => setTimeout(resolve, milliseconds));
}

getData();