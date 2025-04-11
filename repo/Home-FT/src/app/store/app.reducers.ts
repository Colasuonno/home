import {databaseReducers} from './database/database.reducers';
import {profileReducers} from './profile/profile.reducers';

export const reducers = {
  ["database"]: databaseReducers,
  ["profile"]: profileReducers,
}
