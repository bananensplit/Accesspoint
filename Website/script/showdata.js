'use strict';

let mylabels = [];
let myhours = [];

getUpHours()

function getUpHours() {
    let xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            let data = JSON.parse(this.responseText);
            data.data.forEach((element) => {
                mylabels.push(element.date);
                myhours.push(element.hours);
            });
            myChart.update();
        }
    }
    xhttp.open("POST", "getUpHours.php", true)
    xhttp.send()
}


let mycolors = ['#33E0E0', '#FFBD26', '#E04B3F'];
let ctx = document.getElementById('upHoursChart').getContext('2d');
let myChart = new Chart(ctx, {
    type: 'bar',
    data: {
        labels: mylabels,
        datasets: [
            {
                label: 'hours online',
                data: myhours,
                backgroundColor: function (context) {
                    let value = context.dataset.data[context.dataIndex];
                    return mycolors[Math.ceil(value / 8) - 1];
                },
                borderWidth: 0,
                maxBarThickness: 20,
            },
        ]
    },
    options: {
        title: {
            display: true,
            text: 'UP-Time of Raspberry',
            fontSize: 16,
            fontColor: '#242424',
            fontFamily: 'Poppins'
        },
        legend: {
            position: 'right',
            labels: {
                fontFamily: 'Poppins',
                generateLabels: function (context) {
                    let hidden = context.data.datasets[0]._meta[0].hidden;
                    return [
                        {
                            text: '<8 hours',
                            datasetIndex: 0,
                            fillStyle: mycolors[0],
                            hidden: hidden,
                            strokeStyle: 'rgba(0,0,0,0)',
                        },
                        {
                            text: ' 8-16 hours',
                            datasetIndex: 0,
                            fillStyle: mycolors[1],
                            hidden: hidden,
                            strokeStyle: 'rgba(0,0,0,0)',
                        },
                        {
                            text: '16-24 hours',
                            datasetIndex: 0,
                            fillStyle: mycolors[2],
                            hidden: hidden,
                            strokeStyle: 'rgba(0,0,0,0)',
                        }];
                }
            }
        },
        scales: {
            xAxes: [{
                ticks: {
                    fontFamily: 'Poppins',
                },
            }],
            yAxes: [{
                ticks: {
                    beginAtZero: true,
                    max: 24,
                    callback: function (value, index, values) {
                        return value + "h";
                    },
                    fontFamily: 'Poppins',
                },
            }],
        }
    },
});