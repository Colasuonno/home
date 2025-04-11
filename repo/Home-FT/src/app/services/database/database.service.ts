import {inject, Injectable, Signal, WritableSignal} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {homeHost} from '../../app.config';
import Session from '../../model/profile/session';
import {Observable} from 'rxjs';
import {selectDatabaseError} from '../../store/database/database.selectors';
import {Store} from '@ngrx/store';
import {AppState} from '../../store/app.state';

@Injectable({
  providedIn: 'root'
})
export class DatabaseService {

  private store: Store<AppState> = inject(Store);

  public databaseError: Signal<string | undefined> = this.store.selectSignal(selectDatabaseError);

}
