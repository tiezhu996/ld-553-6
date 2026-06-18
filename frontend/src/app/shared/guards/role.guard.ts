import { Injectable } from '@angular/core';
import { ActivatedRouteSnapshot, CanActivate, Router } from '@angular/router';
import { AuthService } from '../services/auth.service';
import { UserRole } from '../constants/enums';

@Injectable({ providedIn: 'root' })
export class RoleGuard implements CanActivate {
  constructor(private auth: AuthService, private router: Router) {}
  canActivate(route: ActivatedRouteSnapshot): boolean {
    const roles = (route.data['roles'] || []) as UserRole[];
    if (!roles.length || this.auth.hasRole(roles)) return true;
    this.router.navigate(['/map']);
    return false;
  }
}
