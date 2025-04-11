import {Component, inject} from '@angular/core';
import {NavbarComponent} from './navbar/navbar.component';
import {ProfileService} from '../../services/profile/profile.service';
import {LoginModalComponent} from './login/login-modal/login-modal.component';

@Component({
  selector: 'app-home',
  imports: [
    NavbarComponent,
    LoginModalComponent
  ],
  templateUrl: './home.component.html',
  styleUrl: './home.component.css'
})
export class HomeComponent {

  protected profileService: ProfileService = inject(ProfileService);



}
