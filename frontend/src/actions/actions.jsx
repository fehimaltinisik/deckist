import ACTION from './definitions'
import axios from "axios";
import {INITIAL_STATE_HELPER_ROUTE_SEGMENTS} from "../constants.js";


const getRandomColor = () => {
    const predefinedColors = [
        // Red
        [255, 102, 102], // #FF6666
        [255, 51, 51],   // #FF3333
        [230, 0, 0],     // #E60000
        [179, 0, 0],     // #B30000
        // [128, 0, 0],     // #800000
        // Orange
        [255, 179, 102], // #FFB366
        [255, 153, 51],  // #FF9933
        [255, 128, 0],   // #FF8000
        [204, 102, 0],   // #CC6600
        // [153, 76, 0],    // #994C00
        // Purple
        [204, 153, 255], // #CC99FF
        [153, 102, 255], // #9966FF
        [102, 51, 204],  // #6633CC
        [76, 46, 102],   // #4C2E66
        [51, 26, 51],    // #331A33
        // Pink
        [255, 153, 204], // #FF99CC
        [255, 102, 178], // #FF66B2
        [255, 51, 153],  // #FF3399
        // [204, 0, 102],   // #CC0066
        // [153, 0, 76],    // #99004C
        // Green
        [153, 255, 153], // #99FF99
        [102, 255, 102], // #66FF66
        [51, 204, 51],   // #33CC33
        // [0, 128, 0],     // #008000
        // [0, 77, 0],      // #004D00
        // Yellow
        [255, 255, 153], // #FFFF99
        [255, 255, 102], // #FFFF66
        [255, 204, 51],  // #FFCC33
        // [204, 153, 0],   // #CC9900
        // [153, 102, 0],   // #996600
        // Violet
        [204, 153, 255], // #CC99FF
        [153, 102, 255], // #9966FF
        // [102, 51, 204],  // #6633CC
        // [76, 46, 102],   // #4C2E66
        // [51, 26, 51]     // #331A33

    ];

    const randomIndex = Math.floor(Math.random() * predefinedColors.length);

    return predefinedColors[randomIndex];
};


export const waitUntilRouteSegmentsLoaded = () =>{
    return async (dispatch) => {
        dispatch({
            type: ACTION.FETCH_ROUTE_SEGMENTS_BY_ROUTE_SHORT_NAME_LOADING
        });
    }
}

export const fetchRouteSegmentsByRouteShortName = ({routeShortName}) => {
    return async (dispatch) => {
        try {
            console.debug(`Fetching route segments for route short name: ${routeShortName}`);
            const url = `${import.meta.env.VITE_BACKEND_SERVICE_URL}/deck/trip-geometries?routeShortName=${routeShortName}`
            const response = await axios.get(url);
            console.debug(`Fetched route segments for route short name: ${routeShortName}`);

            dispatch({
                type: ACTION.FETCH_ROUTE_SEGMENTS_BY_ROUTE_SHORT_NAME_SUCCESS,
                payload: {routeShortName, layerDetails: {segments: response.data, color: getRandomColor()}}
            });
        } catch (error) {
            console.error(error);
            dispatch({type: ACTION.FETCH_ROUTE_SEGMENTS_BY_ROUTE_SHORT_NAME_ERROR, payload: error.message});
        }
    };
}

export const setRefreshRate = (refreshRate) => {
    return (dispatch) => {
        dispatch({
            type: ACTION.ON_REFRESH_RATE_CHANGE,
            payload: refreshRate,
        });
    }
}

export const changeRouteTrailColor = (routeShortName) => {
    return (dispatch) => {
        dispatch({
            type: ACTION.ON_CHANGE_ROUTE_TRAIL_COLOR,
            payload: {routeShortName, color: getRandomColor()}
        });
    }
}

export const setAnimationSpeed = (animationSpeed) => {
    return (dispatch) => {
        dispatch({
            type: ACTION.ON_ANIMATION_SPEED_CHANGE,
            payload: animationSpeed,
        });
    }
}

export const setTrailLength = (trailLength) => {
    return (dispatch) => {
        dispatch({
            type: ACTION.ON_TRAIL_LENGTH_CHANGE,
            payload: trailLength,
        });
    }
}

export const setUserTimeInput = (time) => {
    return (dispatch) => {
        dispatch({
            type: ACTION.ON_TIME_CHANGE,
            payload: time,
        });
    }
}


export const fetchNextHelperRouteSegments = () => {
    return async (dispatch) => {
        if (INITIAL_STATE_HELPER_ROUTE_SEGMENTS.length === 0) {
            console.debug('No more route segments to fetch.')
            return
        }

        try {
            const routeShortName = INITIAL_STATE_HELPER_ROUTE_SEGMENTS.pop()
            console.debug(`Fetching segments of ${routeShortName}...`);
            const response = await axios.get(`${import.meta.env.VITE_S3_BUCKET_URL}/deck/${routeShortName}-route.json`);
            console.debug(`Fetched segments of ${routeShortName}.`);
            console.debug(`${response.data.length} segments of ${routeShortName} found..`);
            dispatch({
                type: ACTION.FETCH_INITIAL_ROUTE_SEGMENTS_SUCCESS,
                payload: {routeShortName: routeShortName, layerDetails: {segments: response.data, color: getRandomColor()}}
            });
        } catch (error) {
            console.error(error);
            dispatch({type: ACTION.FETCH_INITIAL_ROUTE_SEGMENTS_ERROR, payload: error.message});
        }
    }
}


export const addRouteSegmentsByRouteShortName = ({routeShortName}) => ({
    type: ACTION.ADD_ROUTE_SEGMENTS_BY_ROUTE_SHORT_NAME,
    payload: routeShortName,
});

export const removeRouteSegmentsByRouteShortName = ({routeShortName}) => ({
    type: ACTION.REMOVE_ROUTE_SEGMENTS_BY_ROUTE_SHORT_NAME,
    payload: routeShortName,
});