import { useEffect, useState } from "react";
import "./State.css";

function State({ state }) {
    const [className, setClassName] = useState("orange");

    useEffect(() => {
        switch (state) {
            case "active":
                setClassName("on");
                break;
            case "inactive":
                setClassName("off");
                break;

            default:
                setClassName("other");
        }
    }, [state]);

    return <div className={`state ${className}`}>{state}</div>;
}

export default State;
