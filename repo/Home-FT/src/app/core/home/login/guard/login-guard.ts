import {inject, Injectable} from '@angular/core';
import { CanActivate, Router } from '@angular/router';


@Injectable({
  providedIn: 'root',
})
export class LoginGuard implements CanActivate {

  private router: Router = inject(Router);

  async canActivate(): Promise<boolean> {
    if (true) { // TODCO: CHECK LOGGED
      this.router.navigate(['/login']);
      return false;
    } else {
      this.router.navigate(['/login']);
      return false;
    }
  }
}
