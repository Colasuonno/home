import {inject, Injectable, Signal} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {homeHost} from '../../app.config';
import Session from '../../model/profile/session';
import {Observable} from 'rxjs';
import {AppState} from '../../store/app.state';
import {Store} from '@ngrx/store';
import {selectSession} from '../../store/profile/profile.selectors';
import {AuthenticationResponseJSON, startAuthentication} from '@simplewebauthn/browser';
import {requestLoginOptions} from '../../store/profile/profile.actions';

@Injectable({
  providedIn: 'root'
})
export class LoginService {

  private store: Store<AppState> = inject(Store);


  public authenticate(name: string) {
    this.store.dispatch(requestLoginOptions({name: name}))
  }

}
