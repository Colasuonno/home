import {ProfileEffects} from './store/profile/profile.effects';
import {databaseReducers} from './store/database/database.reducers';
import {profileReducers} from './store/profile/profile.reducers';

export const effects = [ProfileEffects]

export const reducers = {
  ["database"]: databaseReducers,
  ["profile"]: profileReducers,
}
