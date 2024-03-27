import * as React from 'react';
import CircularProgress from '@mui/material/CircularProgress';
import Box from '@mui/material/Box';
import {useSelector} from "react-redux";
import {Typography} from "@mui/material";

export default function CircularIndeterminate() {
    const {loadingMessage} = useSelector((state) => state.panel);

    return (
        <Box sx={{display: 'flex', flexDirection: 'column', alignItems: 'center'}}>
            <CircularProgress size='6rem'/>
            <Typography
                size='1rem'
                variant="body1"
                sx={{marginTop: 2}}
            >
                {loadingMessage}
            </Typography>
        </Box>
    );
}