import {inject, Injectable, Signal} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {homeHost} from '../../app.config';
import Session from '../../model/profile/session';
import {Observable} from 'rxjs';
import {AppState} from '../../store/app.state';
import {Store} from '@ngrx/store';
import {selectSession} from '../../store/profile/profile.selectors';
import {
  AuthenticationResponseJSON,
  PublicKeyCredentialRequestOptionsJSON,
  startAuthentication
} from '@simplewebauthn/browser';

@Injectable({
  providedIn: 'root'
})
export class ProfileService {

  private store: Store<AppState> = inject(Store);
  public session: Signal<Session | undefined> =  this.store.selectSignal(selectSession);
  private httpClient: HttpClient = inject(HttpClient);

  public requestOptions(name: string): Observable<PublicKeyCredentialRequestOptionsJSON> {
    console.log("REQUEST OPTIONS")
    return this.httpClient.get<PublicKeyCredentialRequestOptionsJSON>(homeHost + `/auth_options/${name}`)
  }

  public verifyAuth(name: string, authResponse: AuthenticationResponseJSON): Observable<JSON> {
    console.log("VERIFY AUTG")
    console.log(authResponse)
    return this.httpClient.post<JSON>(homeHost + `/auth_options`, {
      login: name,
      credentials: authResponse
    })
  }

  public async authSSHkey(options: PublicKeyCredentialRequestOptionsJSON): Promise<AuthenticationResponseJSON> {
    console.log("auth SSHKEY")
    console.log(options)
    return await startAuthentication({optionsJSON: options});
  }

  public async authPasskey(options: PublicKeyCredentialRequestOptionsJSON): Promise<AuthenticationResponseJSON> {
    console.log("auth")
    console.log(options)
    return await startAuthentication({optionsJSON: options});
  }

}
