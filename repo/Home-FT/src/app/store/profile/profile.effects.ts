import {inject, Injectable} from '@angular/core';
import {Actions, createEffect, ofType} from '@ngrx/effects';
import {loginFailed, loginSuccess, requestLoginOptions, startLogin, verifyLogin} from './profile.actions';
import {catchError, from, map, of, switchMap} from 'rxjs';
import {ProfileService} from '../../services/profile/profile.service';
import LoginType from './model/login-type';

@Injectable()
export class ProfileEffects {
  private actions$ = inject(Actions);
  private profileService = inject(ProfileService);

  verifyLogin$ = createEffect(() => {
    return this.actions$.pipe(
      ofType(verifyLogin),
      switchMap(action =>
        this.profileService.verifyAuth(action.name, action.password, action.credentials)
          .pipe(map(result => {
            console.log("RESULT OF LOGIN")
            console.log(result);


            return loginSuccess({session: undefined})
            }),
            catchError(error => of(loginFailed({error: error.message}))))
      )
    );
  });

  startLogin$ = createEffect(() => {
    return this.actions$.pipe(
      ofType(startLogin),
      switchMap(action => from(action.loginType == LoginType.PASSKEY ?  this.profileService.authPasskey(action.loginOptions) : this.profileService.authPassword(action.loginOptions, action.password!))
        .pipe(map(credentials => verifyLogin({name: action.name, password: action.password, credentials: credentials})),
          catchError(error => of(loginFailed({error: error.message})))))
    );
  });

  requestLoginOptions$ = createEffect(() => {
    return this.actions$.pipe(
      ofType(requestLoginOptions),
      switchMap(action =>
        this.profileService.requestOptions(action.name)
          .pipe(map(options => startLogin({name: action.name, password: action.password, loginOptions: options, loginType: action.loginType})),
            catchError(error => of(loginFailed({error: error.message}))))
      )
    );
  });
}
