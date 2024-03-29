import {useEffect, useState} from 'react';
import {
    Alert,
    Button,
    Checkbox,
    Divider,
    IconButton,
    List,
    ListItem,
    ListItemSecondaryAction,
    ListItemText,
    Slider,
    Stack,
    TextField,
    Tooltip,
    Typography
} from "@mui/material";
import DeleteIcon from '@mui/icons-material/Delete';
import {
    addRouteSegmentsByRouteShortName,
    changeRouteTrailColor,
    fetchNextHelperRouteSegments,
    fetchRouteSegmentsByRouteShortName,
    removeRouteSegmentsByRouteShortName,
    setAnimationSpeed,
    setTrailLength,
    setUserTimeInput,
    waitUntilRouteSegmentsLoaded
} from "../actions/actions.jsx";
import {useDispatch, useSelector} from 'react-redux';
import axios from "axios";
import Box from "@mui/material/Box";
import {
    INITIAL_STATE_ADD_HELPER_ROUTE_SEGMENT_IN_EVERY_X_MS,
    INITIAL_STATE_ANIMATION_SPEED,
    INITIAL_STATE_TRAIL_LENGTH,
    TOTAL_SECONDS_IN_A_DAY
} from "../constants.js";
import {isMobile} from "react-device-detect";


const ANIMATION_SPEED_VALUE_BY_SLIDER_VALUE = {
    0: 0,
    1: 2,
    2: 5,
    3: 10,
}

const rgbToHex = (rgb) => {
    const [r, g, b] = rgb.map(component => component.toString(16).padStart(2, '0'));
    return `#${r}${g}${b}`;
}

const Panel = () => {
    const [showRouteSearchAlert, setShowRouteSearchAlert] = useState(false);
    const [routeSearchAlertMessage, setRouteSearchAlertMessage] = useState('Route not found!');
    const [routeSearchAlertType, setRouteSearchAlertType] = useState('error');
    const [newRouteShortName, setNewNewRouteShortName] = useState('');
    const [isHelpChecked, setIsHelpChecked] = useState(true);
    //
    const {routeShortNames} = useSelector((state) => state.panel);
    const {loading} = useSelector((state) => state.panel);
    const {time: userTimeInput} = useSelector((state) => state.panel);
    const {routeSegmentsByRouteShortName} = useSelector((state) => state.panel);
    //
    const dispatch = useDispatch();

    const isRouteExists = (routeShortName) => {
        return axios.get(`${import.meta.env.VITE_BACKEND_SERVICE_URL}/deck/routes?routeShortName=${routeShortName}`)
            .then((response) => {
                const routes = response.data;
                if (routes.length === 0) {
                    return Promise.resolve(false);
                }
                return Promise.resolve(true);
            }).catch((error) => {
                console.error(error);
                throw error;
            })
    }

    const openRouteSearchAlert = (type, message) => {
        setShowRouteSearchAlert(true);
        setRouteSearchAlertType(type);
        setRouteSearchAlertMessage(message);
    }

    const closeRouteSearchAlert = () => {
        setShowRouteSearchAlert(false);
        setRouteSearchAlertMessage('Route not found!');
    }

    const handleAddNewRoute = (event) => {
        event.preventDefault();
        const isRouteShortNameValid = newRouteShortName.trim() !== '';
        if (!isRouteShortNameValid) {
            setNewNewRouteShortName('');
            console.warn(`Invalid route:${newRouteShortName} route short name!`);
            return;
        }
        isRouteExists(newRouteShortName)
            .then((exists) => {
                if (!exists) {
                    openRouteSearchAlert('error', `Route:${newRouteShortName} not found!`);
                    console.warn(`Route:${newRouteShortName} not found!`);
                    return;
                }
                if (routeShortNames.has(newRouteShortName)) {
                    console.info(`Route:${newRouteShortName} segments already loaded!`);
                    openRouteSearchAlert('info', `Route:${newRouteShortName} already added.`);
                    return;
                }

                console.debug(`Adding route:${newRouteShortName} segments...`);
                dispatch(fetchRouteSegmentsByRouteShortName({routeShortName: newRouteShortName}));
                dispatch(waitUntilRouteSegmentsLoaded());
                dispatch(addRouteSegmentsByRouteShortName({routeShortName: newRouteShortName}))
                dispatch(waitUntilRouteSegmentsLoaded());
                console.debug(`Added route:${newRouteShortName} segments.`);
                closeRouteSearchAlert()
            }).catch(() => {
            openRouteSearchAlert('error', `Error occurred while retrieving route details!`);
        })

        setNewNewRouteShortName('');
    };

    const handleRemoveRoute = (routeShortName) => {
        console.debug(`Removing route:${newRouteShortName} segments!`);
        dispatch(removeRouteSegmentsByRouteShortName({routeShortName}))
    };

    const animationSpeedAriaValueText = (value) => {
        return `${value}m/s`;
    }

    const animationSpeedValueText = (value) => {
        return `${ANIMATION_SPEED_VALUE_BY_SLIDER_VALUE[value]} m/s`;
    }

    const timeValueText = (value) => {
        return value < 10 ? `0${value}:00` : `${value}:00`;
    }

    const timeValueFormat = (time) => {
        const dateUnawareTime = time % TOTAL_SECONDS_IN_A_DAY;
        return Math.trunc(dateUnawareTime / 60 / 60);
    }

    const onChangeAnimationSpeed = (value) => {
        dispatch(setAnimationSpeed(ANIMATION_SPEED_VALUE_BY_SLIDER_VALUE[value]))
    }

    const onChangeTime = (value) => {
        dispatch(setUserTimeInput(value * 60 * 60))
    }

    const onChangeTrailLength = (value) => {
        dispatch(setTrailLength(value))
    }

    const onChangeRouteColor = (routeShortName, color) => {
        routeSegmentsByRouteShortName.get(routeShortName).color = color;
        dispatch(changeRouteTrailColor(routeShortName));
    }

    const handleClearAllRoutes = () => {
        Array.from(routeShortNames).forEach(routeShortName => {
            dispatch(removeRouteSegmentsByRouteShortName({routeShortName}));
        });
    };

    const toggleHelpCheckbox = () => {
        setIsHelpChecked(!isHelpChecked);
    }

    useEffect(() => {
        const intervalId = setInterval(() => {
            if (isHelpChecked) {
                dispatch(fetchNextHelperRouteSegments())
            } else {
                console.debug("Help me mode is disabled.")
            }
        }, INITIAL_STATE_ADD_HELPER_ROUTE_SEGMENT_IN_EVERY_X_MS);

        return () => {
            clearInterval(intervalId);
        }
    }, [isHelpChecked]);

    return (
        <Box
            display='flex'
            flexDirection='column'
            sx={{
                height: isMobile ? "70vh" : '80vh'
            }}
        >
            <Box
                display='flex'
                flexDirection='column'
                sx={{
                    borderRadius: 1,
                    backgroundColor: 'background.paper',
                    flex: 1,
                    minHeight: 0,
                    px: {xs: 3, md: 3},
                    py: {xs: 2, md: 3},
                }}
            >
                <Stack
                    direction="column"
                    spacing={1}
                    display='flex'
                    flexDirection='column'
                    sx={{
                        flex: 1,
                        minHeight: 0,
                        my: {xs: 1, md: 1},
                    }}
                >
                    <Stack
                        direction="column"
                        spacing={1}
                        display='flex'
                        flexDirection='column'
                        sx={{
                            // height: '100%',
                            flex: 1,
                            minHeight: 0,
                        }}
                    >
                        <Typography
                            variant="h6"
                            component="h6"
                            align="left"
                        >
                            Routes
                        </Typography>
                        <Stack
                            direction="row"
                            alignItems="center"
                            spacing={2}
                        >
                            <TextField
                                label="Try 500T"
                                variant="outlined"
                                size="small"
                                disabled={loading}
                                value={newRouteShortName}
                                onChange={(e) => setNewNewRouteShortName(e.target.value.toUpperCase())}
                            />
                            <Button
                                variant="contained"
                                color="primary"
                                size="medium"
                                disabled={loading}
                                onClick={handleAddNewRoute}
                            >
                                Add
                            </Button>
                        </Stack>
                        {
                            showRouteSearchAlert && (
                                <Alert
                                    severity={routeSearchAlertType}
                                    onClose={() => {
                                        closeRouteSearchAlert();
                                    }}
                                    sx={{
                                        textAlign: 'left',
                                    }}
                                >
                                    {routeSearchAlertMessage}
                                </Alert>
                            )
                        }
                        <List
                            sx={{
                                flex: 1,
                                // maxHeight: '33vh',
                                // display="inline-flex"
                                overflow: 'auto',
                                marginBlockStart: '0.5em',
                                paddingInlineStart: '0.5em'
                            }}
                        >
                            {
                                Array.from(routeShortNames).map((routeShortName, index) => (
                                    <ListItem
                                        key={index}
                                        sx={{py: 0}}
                                    >
                                        <Tooltip title="Click to Change Color">
                                            <Box
                                                sx={{
                                                    height: '1em',
                                                    width: '1em',
                                                    bgcolor: rgbToHex(routeSegmentsByRouteShortName.get(routeShortName)?.color || [255, 255, 255]),
                                                    'marginRight': '0.5em',
                                                    px: {xs: 0, md: 0},
                                                }}
                                                onClick={() => onChangeRouteColor(routeShortName)}
                                            >
                                            </Box>
                                        </Tooltip>
                                        <ListItemText primary={routeShortName}/>
                                        <ListItemSecondaryAction>
                                            <IconButton
                                                edge="end"
                                                aria-label="delete"
                                                onClick={() => handleRemoveRoute(routeShortName)}
                                            >
                                                <DeleteIcon/>
                                            </IconButton>
                                        </ListItemSecondaryAction>
                                    </ListItem>
                                ))
                            }
                        </List>
                        <Button
                            variant="contained"
                            color="error"
                            size="medium"
                            disabled={loading || routeShortNames.size === 0}
                            onClick={handleClearAllRoutes}
                            sx={{
                                marginTop: 1,
                            }}
                        >
                            Clear All
                        </Button>
                        <Stack
                            direction="row"
                            alignItems='center'
                            justifyContent='space-between'
                        >
                            <Typography
                                variant="p"
                                component="p"
                                textAlign="right"
                            >
                                Add routes in
                                every {INITIAL_STATE_ADD_HELPER_ROUTE_SEGMENT_IN_EVERY_X_MS / 1000} seconds
                            </Typography>
                            <Checkbox
                                checked={isHelpChecked}
                                onChange={toggleHelpCheckbox}
                            />
                        </Stack>
                    </Stack>

                    <Divider/>
                    <Stack
                        direction="column"
                        style={{
                            flex: 0
                        }}
                    >
                        <Typography
                            variant="h6"
                            component="h6"
                            align="left"
                        >
                            Display Options
                        </Typography>
                        <Stack
                            direction="row"
                            spacing={1.5}
                            alignItems='center'
                        >
                            <Slider
                                aria-label="Time"
                                value={timeValueFormat(userTimeInput)}
                                getAriaValueText={timeValueText}
                                valueLabelDisplay="auto"
                                valueLabelFormat={timeValueText}
                                step={1}
                                min={0}
                                max={23}
                                marks={true}
                                onChange={(e, value) => onChangeTime(value)}
                            />
                            <Typography
                                variant="p"
                                component="p"
                            >
                                Time
                            </Typography>
                        </Stack>
                        <Stack
                            direction="row"
                            spacing={1.5}
                            alignItems='center'
                        >
                            <Slider
                                aria-label="Animation Speed (ms)"
                                defaultValue={INITIAL_STATE_ANIMATION_SPEED}
                                getAriaValueText={animationSpeedAriaValueText}
                                valueLabelFormat={animationSpeedValueText}
                                step={1}
                                min={0}
                                max={3}
                                valueLabelDisplay="auto"
                                onChange={(e, value) => onChangeAnimationSpeed(value)}
                            />
                            <Typography
                                variant="p"
                                component="p"
                                textAlign="right"
                            >
                                AnimationSpeed
                            </Typography>
                        </Stack>
                        <Stack
                            direction="row"
                            spacing={1.5}
                            alignItems='center'
                        >
                            <Slider
                                aria-label="Trail Lenght"
                                defaultValue={INITIAL_STATE_TRAIL_LENGTH}
                                min={20}
                                step={5}
                                max={120}
                                valueLabelDisplay="auto"
                                onChange={(e, value) => onChangeTrailLength(value)}
                            />
                            <Typography
                                variant="p"
                                component="p"
                                textAlign="right"
                            >
                                TrailLength
                            </Typography>
                        </Stack>
                    </Stack>
                </Stack>
            </Box>


        </Box>
    )
        ;
};

export default Panel;
