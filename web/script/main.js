'use strict';

setInterval(getData, 1000)

let socketGeneralInfo = new MyWebsocket('ws://192.168.0.100:3000')

async function getData() {
    while (!socketGeneralInfo.checkIfUp()) {
        await sleep(1000)
    }
    socketGeneralInfo.getData('generalinfo').then(value => {
        let data = JSON.parse(value.data).data
        setState(data.status, false)
        setRuntimeAP(data.status, data.runtime.AP, false)
        setRuntime(data.runtime.pi, false)
        setClients(data.clients, false)
    })
}


function setState(state, waiting) {
    let element = document.querySelector(".show.state")

    if (waiting) {
        element.innerHTML = '<div class="waiting"></div>'
        element.className = 'show state'
        return
    }

    if (state === 'active') {
        element.innerHTML = 'ON'
        element.className = 'show state on'
    } else if (state === 'inactive') {
        element.innerHTML = 'OFF'
        element.className = 'show state off'
    } else {
        element.innerHTML = 'OTHER'
        element.className = 'show state other'
    }
}

function setRuntimeAP(state, time, waiting) {
    if (waiting) {
        let element = document.querySelector(".show.ap-runtime")
        element.innerHTML = '<div class="waiting"></div>'
        element.className = 'show ap-runtime'
        return
    }
    document.querySelector(".show.ap-runtime").innerHTML = state === 'active' ? formatTime(time) : '-'
}

function setRuntime(time, waiting) {
    if (waiting) {
        let element = document.querySelector(".show.runtime")
        element.innerHTML = '<div class="waiting"></div>'
        element.className = 'show runtime'
        return
    }
    document.querySelector(".show.runtime").innerHTML = formatTime(time)
}

function setClients(count, waiting) {
    if (waiting) {
        let element = document.querySelector(".show.client")
        element.innerHTML = '<div class="waiting"></div>'
        element.className = 'show client'
        return
    }
    document.querySelector(".show.client").innerHTML = count
}


function changestateAP(state) {
    let xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            getData()
        }
    }
    xhttp.open('POST', 'start.php', true)
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded")
    xhttp.send(`do=${state ? 'start' : 'stop'}`)
}

function formatTime(date) {
    date = moment().utc().valueOf() - moment(date).utc().valueOf();

    let weeks = Math.floor(date / 1000 / 60 / 60 / 24 / 7)
    let days = Math.floor(date / 1000 / 60 / 60 / 24 % 7)
    let hours = Math.floor(date / 1000 / 60 / 60 % 24)
    let minutes = Math.floor(date / 1000 / 60 % 60)
    let seconds = Math.floor(date / 1000 % 60)

    if (weeks > 0) {
        return `${weeks} week${weeks > 1 ? 's' : ''} ${days} day${days > 1 ? 's' : ''}`
    }
    if (days > 0) {
        return `${days} day${days > 1 ? 's' : ''} ${hours} hour${hours > 1 ? 's' : ''}`
    }
    if (hours > 0) {
        return `${hours} hour${hours > 1 ? 's' : ''} ${minutes} min${minutes > 1 ? 's' : ''}`
    }
    if (minutes > 0) {
        return `${minutes} min${minutes > 1 ? 's' : ''} ${seconds} sec${seconds > 1 ? 's' : ''}`
    }
    return `${seconds} sec${seconds > 1 ? 's' : ''}`
}