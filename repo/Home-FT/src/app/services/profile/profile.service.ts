import {inject, Injectable, Signal} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {homeHost} from '../../app.config';
import Session from '../../model/profile/session';
import {Observable} from 'rxjs';
import {AppState} from '../../store/app.state';
import {Store} from '@ngrx/store';
import {selectSession} from '../../store/profile/profile.selectors';

@Injectable({
  providedIn: 'root'
})
export class ProfileService {

  private store: Store<AppState> = inject(Store);
  public session: Signal<Session | undefined> =  this.store.selectSignal(selectSession);
  private httpClient: HttpClient = inject(HttpClient);

  public login(name: string, timestamp: string, signature: string): Observable<Session> {
    return this.httpClient.post<Session>(homeHost + "/ssh_login", {
      login: name,
      timestamp: timestamp,
      signature: signature
    })
  }

}
