import {combineReducers} from 'redux';
import {reducer as panelReducer} from './Panel.jsx';

const reducer = combineReducers({
    panel: panelReducer,
});

export default reducer;
