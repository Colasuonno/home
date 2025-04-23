import {Component, inject} from '@angular/core';
import {NavbarComponent} from './navbar/navbar.component';
import {ProfileService} from '../../services/profile/profile.service';

@Component({
  selector: 'app-home',
  imports: [
    NavbarComponent,
  ],
  templateUrl: './home.component.html',
  styleUrl: './home.component.css'
})
export default class HomeComponent {

  protected profileService: ProfileService = inject(ProfileService);



}
