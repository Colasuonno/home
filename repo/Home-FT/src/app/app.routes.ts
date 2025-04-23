import { Routes } from '@angular/router';
import {LoginGuard} from './core/home/login/guard/login-guard';

export const routes: Routes = [
  {
    path: '',
    loadComponent: () => import('./core/home/home.component'),
    canActivate: [LoginGuard],
  },
  {
    path: 'login',
    loadComponent: () => import('./core/home/login/login-modal/login-modal.component'),
  }
];
