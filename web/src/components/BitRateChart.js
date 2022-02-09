import { Line } from "@nivo/line";

function BitRateChart({ data }) {
    return (
        <Line
            width={200}
            height={30}
            data={data}
            margin={{ top: 0, right: 0, bottom: 0, left: 0 }}
            // xScale={{ type: "time", format: "%Q" }}
            xScale={{ type: "point" }}
            yScale={{
                type: "linear",
                min: "0",
                max: "80",
                stacked: false,
                reverse: false,
            }}
            xFormat="time:%H:%M:%S.%L"
            enableGridX={false}
            enableGridY={false}
            curve="monotoneX"
            axisTop={null}
            axisRight={null}
            axisBottom={null}
            axisLeft={null}
            enablePoints={false}
            enableArea={true}
            useMesh={true}
            enableSlices="x"
            animate={false}
            colors={["hsl(24, 100%, 50%)"]}
            sliceTooltip={({ slice }) => (
                <div
                    style={{
                        background: "white",
                        padding: "9px 12px",
                        border: "1px solid #ccc",
                        textAlign: "left",
                    }}
                    key={slice.points[0].id}
                >
                    x: {slice.points[0].data.xFormatted}
                    <br />
                    <strong>{slice.points[0].serieId}</strong> {slice.points[0].data.yFormatted}
                </div>
            )}
        />
    );
}

export default BitRateChart;
