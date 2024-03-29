import {Link, ThemeProvider, Typography} from "@mui/material";
import {DARK_THEME} from "../constants.js";

export default function Footer() {
    const year = new Date().getFullYear();

    return (
        <ThemeProvider theme={DARK_THEME}>
            <Typography variant="body2" color="text.secondary" align="center">
                {'Copyright © '}
                <Link
                    variant="a"
                    href="https://www.linkedin.com/in/fehim-alt%C4%B1n%C4%B1%C5%9F%C4%B1k-185802130"
                    target="_blank"
                    rel="noopener"
                    underline="hover"
                >
                    Fehim Altınışık
                </Link>
                {` ${year}.`}

            </Typography>
        </ThemeProvider>
    );
}