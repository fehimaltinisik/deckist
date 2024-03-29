import {Link, Stack, Typography} from "@mui/material";
import {isMobile} from "react-device-detect";

export default function MapAreaFooter() {
    return (
        <Stack
            direction="row"
            alignItems="center"
            style={{
                position: "absolute", left: '0em', bottom: '0em', zIndex: 1,
            }}
            sx={{
                px: {xs: 3, md: 3},
            }}
        >
            <Typography
                variant="body2"
                component="body2"
            >
                DeckIst{!isMobile && "  "}&nbsp;-{!isMobile && "  "}&nbsp;
            </Typography>
            <Typography
                variant="body2"
                component="body2"
            >
                Source code {!isMobile && "available"}&nbsp;@&nbsp;
            </Typography>
            <Link
                variant="body2"
                component="a"
                href=""
                target="_blank"
                rel="noopener"
                underline="hover"
            >
                GitHub
            </Link>
            {
                !isMobile && (
                    <>
                        <Typography
                            variant="body2"
                            component="body2"
                        >
                            &nbsp;&nbsp;&nbsp;-&nbsp;&nbsp;&nbsp;Made possible with&nbsp;
                        </Typography>
                        <Link
                            variant="body2"
                            component="a"
                            href="https://deck.gl/"
                            target="_blank"
                            rel="noopener"
                            underline="hover"
                        >
                            deck.gl
                        </Link>
                        <Typography
                            variant="body2"
                            component="body2"
                        >
                            &nbsp;and&nbsp;Istanbul&nbsp;
                        </Typography>
                        <Link
                            variant="body2"
                            component="a"
                            href="https://data.ibb.gov.tr/dataset/public-transport-gtfs-data"
                            target="_blank"
                            rel="noopener"
                            underline="hover"
                        >
                            GTFS
                        </Link>
                        <Typography
                            variant="body2"
                            component="body2"
                        >
                            &nbsp;Data
                        </Typography>
                    </>
                )
            }
        </Stack>
    );
}