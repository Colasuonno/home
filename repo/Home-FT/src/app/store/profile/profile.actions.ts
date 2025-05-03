import {createAction, props} from '@ngrx/store';
import Session from '../../model/profile/session';
import {
  AuthenticationCredential,
  AuthenticationResponseJSON,
  PublicKeyCredentialRequestOptionsJSON
} from '@simplewebauthn/browser';
import LoginType from './model/login-type';

export const requestLoginOptions = createAction(
  'EXTERNAL_REQUEST_LOGIN_OPTIONS',
  props<{ name: string, password: string | undefined, loginType: LoginType }>()
);

export const startLogin = createAction(
  'EXTERNAL_REQUEST_START_LOGIN',
  props<{ name: string, password: string | undefined, loginOptions: PublicKeyCredentialRequestOptionsJSON, loginType: LoginType }>()
);

export const verifyLogin = createAction(
  'EXTERNAL_REQUEST_VERIFY_LOGIN',
  props<{ name: string, password: string | undefined, credentials: AuthenticationResponseJSON | boolean }>()
);

export const loginSuccess = createAction(
  'INTERNAL_LOGIN_SUCCESS',
  props<{ session: Session | undefined }>()
);


export const loginFailed = createAction(
  'INTERNAL_LOGIN_FAILED',
  props<{ error: string | undefined }>()
);



