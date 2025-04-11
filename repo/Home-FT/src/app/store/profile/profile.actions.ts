import {createAction, props} from '@ngrx/store';
import Session from '../../model/profile/session';

export const login = createAction(
  'EXTERNAL_LOGIN_KEY',
  props<{ name: string, timestamp: string, signature: string }>()
);


export const loginSuccess = createAction(
  'INTERNAL_LOGIN_SUCCESS',
  props<{ session: Session }>()
);


export const loginFailed = createAction(
  'INTERNAL_LOGIN_FAILED',
  props<{ error: string | undefined }>()
);



