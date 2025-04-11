import {AfterViewInit, Component, inject, Input, OnInit, signal, WritableSignal} from '@angular/core';
import {FormsModule} from '@angular/forms';
import {AppState} from '../../../../store/app.state';
import {Store} from '@ngrx/store';
import {login} from '../../../../store/profile/profile.actions';
import {DatabaseService} from '../../../../services/database/database.service';
import {AlertComponent} from '../../../../shared/alert/alert.component';

@Component({
  selector: 'app-login-modal',
  imports: [
    FormsModule,
    AlertComponent
  ],
  templateUrl: './login-modal.component.html',
  styleUrl: './login-modal.component.css'
})
export class LoginModalComponent implements AfterViewInit {

  protected name: WritableSignal<string> = signal('')
  protected timestamp: WritableSignal<string> = signal('')
  protected signature: WritableSignal<string> = signal('')

  protected databaseService: DatabaseService = inject(DatabaseService);
  private store: Store<AppState> = inject(Store);

  ngAfterViewInit() {
    const modal = this.obtainModal();
    modal.close()
    modal.showModal();
  }

  protected obtainModal(): HTMLDialogElement {
    return document.getElementById("login-modal") as HTMLDialogElement;
  }

  protected login(): void {

    console.log(this.name())
    console.log(this.timestamp())
    console.log(this.signature())

    this.store.dispatch(login({name: this.name(), signature: this.signature(), timestamp: this.timestamp()}))

  }


}
