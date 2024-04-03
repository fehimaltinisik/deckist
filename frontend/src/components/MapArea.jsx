import {useEffect, useState} from 'react';
import {MapContext, NavigationControl, StaticMap} from 'react-map-gl';
import {DeckGL} from 'deck.gl';
import {useDispatch, useSelector} from "react-redux";
import {TripsLayer} from '@deck.gl/geo-layers';
import {createTheme, Paper, Stack, ThemeProvider, Typography} from "@mui/material";
import {setUserTimeInput} from "../actions/actions.jsx";
import Box from "@mui/material/Box";
import CircularIndeterminate from "./CircularIntermediate.jsx";
import UpdateIcon from "@mui/icons-material/Update.js";
import {DARK_THEME, INITIAL_STATE_TIME_IN_SECONDS, TOTAL_SECONDS_IN_A_DAY} from "../constants.js";
import {isMobile} from 'react-device-detect';
import MapAreaFooter from "./MapAreaFooter.jsx";


const digitalClockText = (timestamp) => {
    const hours = Math.trunc(timestamp / 3600)
    const hours_modulated = Math.trunc(timestamp / 3600) % 24
    const minutes = Math.trunc((timestamp - hours * 3600) / 60)
    const hoursText = hours_modulated < 10 ? `0${hours_modulated}` : `${hours_modulated}`
    const minutesText = minutes < 10 ? `0${minutes}` : `${minutes}`

    return `${hoursText}:${minutesText}`
}

const resolveOpacity = (isLoading) => {
    return isLoading ? 0.35 : 1.0;
}

const INITIAL_VIEW_STATE = {
    latitude: 41.031852773133515,
    longitude: 29.079875038786454,
    zoom: 10,
    bearing: 2.1192893401015205,
    pitch: 37.374216241015446
};

const MAP_STYLE = 'https://basemaps.cartocdn.com/gl/dark-matter-nolabels-gl-style/style.json';
const NAV_CONTROL_STYLE = {position: 'absolute', top: 10, left: 10};

export default function MapArea() {

    const [time, setTime] = useState(INITIAL_STATE_TIME_IN_SECONDS);
    const [animation] = useState({});
    //
    const {loading} = useSelector((state) => state.panel);
    const {routeSegmentsByRouteShortName} = useSelector((state) => state.panel);
    const {refreshRate} = useSelector((state) => state.panel);
    const {trailLength, animationSpeed, time: userTimeInput} = useSelector((state) => state.panel);
    //
    const dispatch = useDispatch();

    useEffect(() => {
        setTime(userTimeInput)
        console.log('Refreshing animation component...')

        // eslint-disable-next-line no-unused-vars
        const animate = (_) => {
            const resolveNextTimestamp = (timestamp, speed) => {
                // console.debug(`resolveNextTimestamp:${timestamp} animationSpeed:${speed}`)
                const nextTimeStamp = timestamp + speed;
                const isHourly = nextTimeStamp % 3600 === 0;
                if (isHourly) {
                    dispatch(setUserTimeInput(nextTimeStamp));
                }
                if (nextTimeStamp > TOTAL_SECONDS_IN_A_DAY + INITIAL_STATE_TIME_IN_SECONDS) {
                    return nextTimeStamp % (TOTAL_SECONDS_IN_A_DAY);
                }

                return nextTimeStamp;
            }
            setTime(t => resolveNextTimestamp(t, animationSpeed));
            if (refreshRate < 50) {
                setTimeout(() => {
                    animation.id = window.requestAnimationFrame(t => (animate(t)));
                }, 1000 / refreshRate);
            } else {
                animation.id = window.requestAnimationFrame(t => (animate(t)));
            }
        };

        animation.id = window.requestAnimationFrame(t => (animate(t)));
        return () => window.cancelAnimationFrame(animation.id);
    }, [animation, userTimeInput, animationSpeed, refreshRate]);

    const layers = []

    routeSegmentsByRouteShortName.forEach((layerDetails, routeShortName) => {
        const color = layerDetails.color
        layers.push(new TripsLayer({
            id: `${routeShortName}-trip`,
            data: layerDetails.segments,
            getPath: d => d.path,
            getTimestamps: d => d.timestamps,
            getColor: color,
            opacity: 1.0,
            trailLength: trailLength,
            currentTime: time,
            shadowEnabled: false,
            widthMinPixels: 3,
        }));
    })

    return (<Box
        position={!isMobile ? 'static' : 'sticky'}
        sx={{
            display: 'flex',
            flexDirection: 'column',
            height: isMobile ? "60vh" : '80vh',
            width: isMobile ? "100vw" : "75vw",
            justifyContent: 'center',
            alignItems: 'center',
        }}
    >
            <Paper
                style={{
                    display: "flex", flexDirection: "column", alignItems: 'center', justifyContent: 'center', position: "relative", height: "100%", width: "100%",
                }}
            >
                <DeckGL
                    layers={layers}
                    initialViewState={INITIAL_VIEW_STATE}
                    controller={true}
                    ContextProvider={MapContext.Provider}
                    style={{
                        opacity: resolveOpacity(loading),
                    }}
                >
                    <StaticMap mapStyle={MAP_STYLE}/>
                    <NavigationControl style={NAV_CONTROL_STYLE}/>
                </DeckGL>
                <Stack
                    direction="row"
                    spacing={1}
                    alignItems='center'
                    style={{
                        position: "absolute", top: '0.5em', right: '0.75em', zIndex: 1,
                    }}
                >
                    <UpdateIcon
                        fontSize="large"
                    />
                    <Typography
                        variant={!isMobile ? 'h4' : 'h6'}
                        component={!isMobile ? 'h4' : 'h6'}
                    >
                        {digitalClockText(time)}
                    </Typography>
                </Stack>

                <MapAreaFooter

                />
                {loading && <CircularIndeterminate/>}
            </Paper>
    </Box>);
}