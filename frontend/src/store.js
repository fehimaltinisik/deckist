import { reducer as panelReducer } from './reducers/Panel';
import {configureStore} from "@reduxjs/toolkit";

export const store = configureStore({
    reducer: { panel: panelReducer, },
    devTools: true,
    middleware: (getDefaultMiddleware) => getDefaultMiddleware({
        serializableCheck: false,
    }),
})