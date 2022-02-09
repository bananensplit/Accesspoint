import moment from "moment";
import { useState } from "react";
import "./App.css";
import BitRateChart from "./components/BitRateChart";
import DeviceGrid from "./components/DeviecGrid/DeviceGrid";
import State from "./components/State";
import Waiting from "./components/Waiting";
import useInterval from "./hooks/useInterval";
import useWebsocket from "./hooks/useWebsocket";

function App() {
    const [intervalDelay, setIntervalDelay] = useState(null);
    const [intervalDeviceDelay, setIntervalDeviceDelay] = useState(null);
    const [info, setInfo] = useState(null); // Info
    const [devices, setDevices] = useState([]);

    const [rxGraphData, setRxGraphData] = useState({});
    const [txGraphData, setTxGraphData] = useState({});

    useInterval(fetchData, intervalDelay);
    useInterval(fetchDevices, intervalDeviceDelay);

    const ws = useWebsocket(
        "ws.currents://ap.bananensplit.com/api",
        function (event) {
            setIntervalDelay(300);
            setIntervalDeviceDelay(300);
        },
        function (event) {
            setIntervalDelay(null);
            setIntervalDeviceDelay(null);
        },
        function (event) {
            setIntervalDelay(null);
            setIntervalDeviceDelay(null);
        },
        function (event) {
            const data = JSON.parse(event.data);
            if (data?.["type"] === "info") setInfo(data?.data || null);
            if (data?.["type"] === "clients_info") {
                let newTxGraphData = {};
                let newRxGraphData = {};
                data?.data.forEach((i) => {
                    let newTx =
                        txGraphData[i["mac"]] ||
                        new Array(50).fill(0).map((value, index) => ({
                            x: index + "",
                            y: null,
                        }));
                    let newRx =
                        rxGraphData[i["mac"]] ||
                        new Array(50).fill(0).map((value, index) => ({
                            x: index + "",
                            y: null,
                        }));
                    newTx = newTx.slice(1);
                    newRx = newRx.slice(1);
                    newTx.push({
                        x: moment().valueOf() + "",
                        y: i["tx-bitrate"].substr(0, i["tx-bitrate"].length - 6),
                    });
                    newRx.push({
                        x: moment().valueOf() + "",
                        y: i["rx-bitrate"].substr(0, i["rx-bitrate"].length - 6),
                    });
                    newTxGraphData[i["mac"]] = newTx;
                    newRxGraphData[i["mac"]] = newRx;
                });
                setTxGraphData(newTxGraphData);
                setRxGraphData(newRxGraphData);
                setDevices(
                    data?.data.map((i) => ({
                        "connected-time": i["connected-time"],
                        mac: i["mac"],
                        "tx-bitrate": (
                            <>
                                <BitRateChart data={[{ id: "Bandwidth", data: txGraphData[i["mac"]] || [] }]} />
                                {i["tx-bitrate"]}
                            </>
                        ),
                        "rx-bitrate": (
                            <>
                                <BitRateChart data={[{ id: "Bandwidth", data: rxGraphData[i["mac"]] || [] }]} />
                                {i["rx-bitrate"]}
                            </>
                        ),
                        vendor: i["vendor"],
                    })) || []
                );
            }
        }
    );

    function fetchData() {
        ws.current.send(JSON.stringify({ type: "info" }));
    }

    function fetchDevices() {
        ws.current.send(JSON.stringify({ type: "clients_info" }));
    }

    function apUp() {
        ws.current.send(JSON.stringify({ type: "on" }));
    }

    function apDown() {
        ws.current.send(JSON.stringify({ type: "off" }));
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
