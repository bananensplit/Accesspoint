'use strict';

class MyWebsocket {
    constructor(url) {
        this.url = url;
        this.connection = new WebSocket(url)
    }

    getData(request) {
        if (!this.checkIfUp()) {
            return false;
        }

        this.connection.send(request);
        return new Promise(resolve => {
            this.connection.onmessage = ev => resolve(ev);
        })
    }

    close() {
        this.connection.close();
    }

    checkIfUp() {
        return this.connection.readyState === 1;
    }
}