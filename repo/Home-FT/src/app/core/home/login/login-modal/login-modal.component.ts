import {
  AfterViewInit,
  Component,
  EventEmitter,
  inject,
  Input,
  OnInit,
  Output,
  signal,
  WritableSignal
} from '@angular/core';
import {FormsModule} from '@angular/forms';
import {AppState} from '../../../../store/app.state';
import {Store} from '@ngrx/store';
import {DatabaseService} from '../../../../services/database/database.service';
import {AlertComponent} from '../../../../shared/alert/alert.component';
import {LoginService} from '../../../../services/profile/login.service';
import {NavbarComponent} from '../../navbar/navbar.component';
import LoginType from '../../../../store/profile/model/login-type';

@Component({
  selector: 'app-login-modal',
  imports: [
    FormsModule,
    AlertComponent,
    NavbarComponent
  ],
  templateUrl: './login-modal.component.html',
  styleUrl: './login-modal.component.css'
})
export default class LoginModalComponent implements AfterViewInit {

  protected name: WritableSignal<string> = signal('')
  protected password: WritableSignal<string> = signal('')

  protected databaseService: DatabaseService = inject(DatabaseService);
  private store: Store<AppState> = inject(Store);

  private loginService: LoginService = inject(LoginService);

  ngAfterViewInit() {
    const modal = this.obtainModal();
    modal.close()
    modal.showModal();
  }

  protected obtainModal(): HTMLDialogElement {
    return document.getElementById("login-modal") as HTMLDialogElement;
  }

  protected login(loginType: LoginType) {

    this.loginService.authenticate(this.name(), loginType, this.password());
  }


  protected readonly LoginType = LoginType;
}
