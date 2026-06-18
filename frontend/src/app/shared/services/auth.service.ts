import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';
import { Observable, tap } from 'rxjs';
import { environment } from '../../../environments/environment';
import { UserRole } from '../constants/enums';

export interface CurrentUser { id: number; username: string; role: UserRole; }

@Injectable({ providedIn: 'root' })
export class AuthService {
  private tokenKey = 'transithub_token';
  private userKey = 'transithub_user';

  constructor(private http: HttpClient, private router: Router) {}

  login(username: string, password: string): Observable<{ access: string; user: CurrentUser }> {
    return this.http.post<{ access: string; user: CurrentUser }>(`${environment.apiBaseUrl}/auth/login/`, { username, password })
      .pipe(tap(res => {
        localStorage.setItem(this.tokenKey, res.access);
        localStorage.setItem(this.userKey, JSON.stringify(res.user));
      }));
  }

  logout(): void {
    localStorage.removeItem(this.tokenKey);
    localStorage.removeItem(this.userKey);
    this.router.navigate(['/auth/login']);
  }

  token(): string | null { return localStorage.getItem(this.tokenKey); }
  user(): CurrentUser | null { const raw = localStorage.getItem(this.userKey); return raw ? JSON.parse(raw) : null; }
  hasRole(roles: UserRole[]): boolean { const role = this.user()?.role; return !!role && roles.includes(role); }
}
