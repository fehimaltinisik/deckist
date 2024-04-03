import './App.css'
import MapArea from "./components/MapArea.jsx";
import Panel from "./components/Panel.jsx";
import {Stack, ThemeProvider} from "@mui/material";
import {isMobile} from 'react-device-detect';
import Footer from "./components/Footer.jsx";
import {DARK_THEME} from "./constants.js";


function App() {
    return (
        <>
            <ThemeProvider theme={DARK_THEME}>
                <Stack
                    direction="column"
                    spacing={2}
                >
                    <Stack
                        direction={isMobile ? 'column' : 'row'}
                        spacing={2}
                    >
                        <MapArea/>
                        <Panel/>
                    </Stack>
                    <Footer/>
                </Stack>
            </ThemeProvider>
        </>
    )
}

export default App
