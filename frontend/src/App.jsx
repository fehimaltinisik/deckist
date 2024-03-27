import './App.css'
import MapArea from "./components/DeckGLMap.jsx";
import Panel from "./components/Panel.jsx";
import {Stack} from "@mui/material";

function App() {
    return (
        <>
            <Stack
                direction="row"
                spacing={2}
            >
                <MapArea/>
                <Panel/>
            </Stack>
        </>
    )
}

export default App
