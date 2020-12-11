'use strict';

setInterval(getData, 1000)

function getData() {
    let xhttp = new XMLHttpRequest();

    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            let data = JSON.parse(this.responseText)
            setState(data.status, false)
            setRuntimeAP(data.status, data.runtime.AP, false)
            setRuntime(data.runtime.pi, false)
            setClients(data.clients, false)
        }
    }
    xhttp.open("POST", "getData.php", true)
    xhttp.send();
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
        element.innerHTML = 'other'
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
    date = new Date(date)
    return date.toLocaleString()
}