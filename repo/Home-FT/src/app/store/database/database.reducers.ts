import {DatabaseState, ProfileState} from '../app.state';
import {createReducer, on} from '@ngrx/store';
import {login, loginFailed} from '../profile/profile.actions';

export const initialState: DatabaseState = {
  databaseError: undefined,
};

export const databaseReducers = createReducer(
  initialState,
  on(login, (state: DatabaseState) =>  ({...state, databaseError: undefined}) ),
  on(loginFailed, (state: DatabaseState, {error}) =>  ({...state, databaseError: error}) ),
);
