import {inject, Injectable} from '@angular/core';
import {Actions, createEffect, ofType} from '@ngrx/effects';
import {login, loginFailed, loginSuccess} from './profile.actions';
import {catchError, map, of, switchMap} from 'rxjs';
import {ProfileService} from '../../services/profile/profile.service';

@Injectable()
export class ProfileEffects {
  private actions$ = inject(Actions);
  private profileService = inject(ProfileService);

  login$ = createEffect(() => {
    return this.actions$.pipe(
      ofType(login),
      switchMap(action =>
        this.profileService.login(action.name, action.timestamp, action.signature)
          .pipe(map(session => loginSuccess({session})),
            catchError(error => of(loginFailed({error: error.message}))))
      )
    );
  });
}
