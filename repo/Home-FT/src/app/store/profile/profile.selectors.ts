import {AppState, DatabaseState, ProfileState} from '../app.state';
import {createSelector} from '@ngrx/store';

export const root = (state: AppState) => state.profile;

export const selectSession = createSelector(
  root,
  (state: ProfileState) => state.session
);
