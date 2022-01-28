import "./DeviceGrid.css";
import GridRow from "./GridRow";

function DeviceGrid({ data }) {
    return (
        <div className="devicegrid">
            <div className="gridheader">vendor</div>
            <div className="gridheader">connected</div>
            <div className="gridheader">tx</div>
            <div className="gridheader">rx</div>
            <div className="gridheader">mac</div>
            {data.map((i) => <GridRow data={i} />)}
        </div>
    );
}

export default DeviceGrid;
