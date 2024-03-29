import './App.css'
import MapArea from "./components/MapArea.jsx";
import Panel from "./components/Panel.jsx";
import {Stack} from "@mui/material";
import {isMobile} from 'react-device-detect';
import Footer from "./components/Footer.jsx";


function App() {
    return (
        <>
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
        </>
    )
}

export default App
