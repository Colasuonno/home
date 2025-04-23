import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import HomeComponent from './core/home/home.component';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  imports: [
    HomeComponent,
    RouterOutlet
  ],
  styleUrl: './app.component.css'
})
export class AppComponent {

}
