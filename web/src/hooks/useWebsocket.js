import { useEffect, useRef } from "react";

function useWebsocket(uri, onopen, onerror, onclose, onmessage) {
    const websocket = useRef();
    // Setup the websocket
    useEffect(() => {
        websocket.current = new WebSocket("ws://ap.bananensplit.com/api");

        return () => {
            websocket.current.close();
            websocket.current = null;
        };
    }, [uri]);

    useEffect(() => {
        websocket.current.onopen = onopen;
    }, [onopen]);
    useEffect(() => {
        websocket.current.onerror = onerror;
    }, [onerror]);
    useEffect(() => {
        websocket.current.onclose = onclose;
    }, [onclose]);
    useEffect(() => {
        websocket.current.onmessage = onmessage;
    }, [onmessage]);

    return websocket;
}

export default useWebsocket;
