import { Component } from '@angular/core';
import {homeName} from '../../../app.config';

@Component({
  selector: 'app-navbar',
  imports: [],
  templateUrl: './navbar.component.html',
  styleUrl: './navbar.component.css'
})
export class NavbarComponent {

  protected readonly homeName = homeName;
}
