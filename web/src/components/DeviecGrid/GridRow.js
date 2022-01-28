import moment from "moment";
import "./DeviceGrid.css";

function GridRow({ data }) {
    return (
        <>
            <div className="gridcell">{data?.["vendor"] || "unknown"}</div>
            <div className="gridcell">{data?.["connected-time"] ? moment.utc().subtract(data?.["connected-time"], 'seconds').fromNow() : '-'}</div>
            <div className="gridcell">{data?.["tx-bitrate"] || '-'}</div>
            <div className="gridcell">{data?.["rx-bitrate"] || '-'}</div>
            <div className="gridcell">{data?.["mac"] || '-'}</div>
        </>
    );
}

export default GridRow;
