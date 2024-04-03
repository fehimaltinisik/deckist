import ACTION from '../actions/definitions';
import {
    INITIAL_STATE_ANIMATION_SPEED,
    INITIAL_STATE_REFRESH_RATE,
    INITIAL_STATE_TIME_IN_SECONDS,
    INITIAL_STATE_TRAIL_LENGTH
} from "../constants.js";


const initialState = {
    loading: false,
    loadingMessage: 'Progressing...',
    animationSpeed: INITIAL_STATE_ANIMATION_SPEED,
    trailLength: INITIAL_STATE_TRAIL_LENGTH,
    time: INITIAL_STATE_TIME_IN_SECONDS,
    refreshRate: INITIAL_STATE_REFRESH_RATE,
    routeShortNames: new Set(),
    routeSegmentsByRouteShortName: new Map(),
    error: null,
};

const reducer = (state = initialState, action) => {

    switch (action.type) {
        case ACTION.ADD_ROUTE_SEGMENTS_BY_ROUTE_SHORT_NAME:
            return {
                ...state,
                loading: false,
                routeShortNames: state.routeShortNames.add(action.payload),
            };

        case ACTION.REMOVE_ROUTE_SEGMENTS_BY_ROUTE_SHORT_NAME:
            state.routeShortNames.delete(action.payload)
            state.routeSegmentsByRouteShortName.delete(action.payload)

            return {
                ...state,
                loading: false,
            };
        // --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---
        // ---
        // --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---
        case ACTION.FETCH_ROUTE_SEGMENTS_BY_ROUTE_SHORT_NAME_SUCCESS:
            state.routeSegmentsByRouteShortName.set(action.payload.routeShortName, action.payload.layerDetails)

            return {
                ...state,
                loading: false,
                routeSegmentsByRouteShortName: new Map(state.routeSegmentsByRouteShortName)
            };

        case ACTION.FETCH_ROUTE_SEGMENTS_BY_ROUTE_SHORT_NAME_LOADING:
            return {
                ...state,
                loading: true
            };

        case ACTION.FETCH_INITIAL_ROUTE_SEGMENTS_SUCCESS:
            state.routeSegmentsByRouteShortName.set(action.payload.routeShortName, action.payload.layerDetails)

            return {
                ...state,
                loading: false,
                routeSegmentsByRouteShortName: new Map(state.routeSegmentsByRouteShortName),
                routeShortNames: state.routeShortNames.add(action.payload.routeShortName),
            };

        // --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---
        // Panel Actions
        // --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---
        case ACTION.ON_ANIMATION_SPEED_CHANGE:
            console.debug(`Setting animation speed to:${action.payload}`)
            return {
                ...state,
                animationSpeed: action.payload,
            }

        case ACTION.ON_TIME_CHANGE:
            console.debug(`Setting time to:${action.payload}`)
            return {
                ...state,
                time: action.payload,
            }

        case ACTION.ON_TRAIL_LENGTH_CHANGE:
            console.debug(`Setting trail length to:${action.payload}`)
            return {
                ...state,
                trailLength: action.payload,
            }

        case ACTION.ON_CHANGE_ROUTE_TRAIL_COLOR:
            console.debug(`Setting trail color to:${action.payload.color}`)
            state.routeSegmentsByRouteShortName.get(action.payload.routeShortName).color = action.payload.color
            return {
                ...state,
            }

        case ACTION.ON_REFRESH_RATE_CHANGE:
            console.debug(`Setting refresh rate to:${action.payload}`)
            return {
                ...state,
                refreshRate: action.payload,
            }

        default:
            return state;
    }
};


export {reducer};
