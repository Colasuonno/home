import Session from '../model/profile/session';

export interface DatabaseState {
  databaseError: string | undefined;
}

export interface ProfileState {
  session: Session | undefined;
}

export interface AppState {
  profile: ProfileState;
  database: DatabaseState;
}
