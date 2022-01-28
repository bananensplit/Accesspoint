import moment from "moment";
import { useEffect, useState } from "react";
import "./App.css";
import DeviceGrid from "./components/DeviecGrid/DeviceGrid";
import State from "./components/State";
import Waiting from "./components/Waiting";

var ws;

function App() {
    const [intervalId, setIntervalId] = useState(null); // interval id
    const [intervalDeviceId, setIntervalDeviceId] = useState(null); // interval id
    const [info, setInfo] = useState(null); // Info
    const [devices, setDevices] = useState([]); // Info

    useEffect(() => {
        ws = new WebSocket("wss://ap.bananensplit.com/api");

        ws.onopen = function (event) {
            setIntervalId(setInterval(fetchData, 300));
            setIntervalDeviceId(setInterval(fetchDevices, 1000));
        };

        ws.onerror = function (event) {
            clearInterval(intervalId);
            setIntervalId(null);
            setIntervalDeviceId(null);
        };

        ws.onclose = function (event) {
            clearInterval(intervalId);
            setIntervalId(null);
            setIntervalDeviceId(null);
        };

        ws.onmessage = function (event) {
            const data = JSON.parse(event.data);
            if (data?.["type"] === "info") setInfo(data?.data || null);
            if (data?.["type"] === "clients_info") setDevices(data?.data || []);
        };
    }, []);

    function fetchData() {
        ws.send(JSON.stringify({ type: "info" }));
    }

    function fetchDevices() {
        ws.send(JSON.stringify({ type: "clients_info" }));
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
            <div className="container">
                <div id="info-view">
                    <div className="desc">State</div>
                    <div className="show">{info?.["ap-state"] ? <State state={info?.["ap-state"]} /> : <Waiting />}</div>
                    <div className="desc">AP running since</div>
                    <div className="show">
                        {info ? (
                            (info?.["ap-state"] === "active" && info?.["ap-uptime"] && getTimeStr(info["ap-uptime"])) || "-"
                        ) : (
                            <Waiting />
                        )}
                    </div>
                    <div className="desc">PI running since</div>
                    <div className="show">{info?.["pi-uptime"] ? getTimeStr(info?.["pi-uptime"]) : <Waiting />}</div>
                    <div className="desc">Connected Clients</div>
                    <div className="show">{info ? info?.["ap-state"] === "active" ? info?.["clients"] : "-" : <Waiting />}</div>
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
            <div className="nice">Wer das liest ist dumm :D</div>
            <div className="container">
                <DeviceGrid data={devices} />
            </div>
        </div>
    );
}

export default App;
