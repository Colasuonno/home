import {createReducer, on} from '@ngrx/store';
import {ProfileState} from '../app.state';


export const initialState: ProfileState = {
  session: undefined
};

export const profileReducers = createReducer(
  initialState,
);
