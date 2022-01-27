import moment from "moment";
import { useEffect, useState } from "react";
import "./App.css";
import State from "./components/State";
import Waiting from "./components/Waiting";

var ws;

function App() {
    const [intervalId, setIntervalId] = useState(null); // interval id
    const [info, setInfo] = useState(null); // Info

    useEffect(() => {
        ws = new WebSocket("ws://192.168.0.100:8001");

        ws.onopen = function (event) {
            setIntervalId(setInterval(fetchData, 100));
        };

        ws.onerror = function (event) {
            clearInterval(intervalId);
            setIntervalId(null);
        };

        ws.onclose = function (event) {
            clearInterval(intervalId);
            setIntervalId(null);
        };

        ws.onmessage = function (event) {
            const data = JSON.parse(event.data);
            if (data?.["type"] === "info") setInfo(data?.data || null);
        };
    }, []);

    function fetchData() {
        ws.send(JSON.stringify({ type: "info" }));
    }
    function apUp() {
        ws.send(JSON.stringify({ type: "on" }));
    }
    function apDown() {
        ws.send(JSON.stringify({ type: "off" }));
    }

    function getTimeStr(timestamp) {
        return moment.unix(timestamp).fromNow();
    }

    return (
        <div className="App">
            <div id="info-view">
                <div className="desc">State</div>
                <div className="show">{info?.["ap-state"] ? <State state={info?.["ap-state"]} /> : <Waiting />}</div>
                <div className="desc">AP running since</div>
                <div className="show">{info?.["ap-uptime"] ? getTimeStr(info["ap-uptime"]) : <Waiting />}</div>
                <div className="desc">PI running since</div>
                <div className="show">{info?.["pi-uptime"] ? getTimeStr(info?.["pi-uptime"]) : <Waiting />}</div>
                <div className="desc">Connected Clients</div>
                <div className="show">{info?.["clients"] || <Waiting />}</div>
            </div>
            <div id="controls">
                <button onClick={apUp} className={"onBtn"}>
                    turn on
                </button>
                <button onClick={apDown} className={"offBtn"}>
                    turn off
                </button>
            </div>
        </div>
    );
}

export default App;
