import {createReducer, on} from '@ngrx/store';
import {ProfileState} from '../app.state';
import {loginSuccess} from './profile.actions';


export const initialState: ProfileState = {
  session: undefined
};

export const profileReducers = createReducer(
  initialState,
);
