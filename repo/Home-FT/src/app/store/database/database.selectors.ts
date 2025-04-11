import {AppState, DatabaseState} from '../app.state';
import {createSelector} from '@ngrx/store';

export const root = (state: AppState) => state.database;

export const selectDatabaseError = createSelector(
  root,
  (state: DatabaseState) => state.databaseError
);
