import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { AuthService } from '../../shared/services/auth.service';

@Component({ standalone: false,
  template: `<section class="login"><form class="panel" (ngSubmit)="submit()"><h1>TransitHub 登录</h1><mat-form-field><mat-label>账号</mat-label><input matInput name="username" [(ngModel)]="username"></mat-form-field><mat-form-field><mat-label>密码</mat-label><input matInput type="password" name="password" [(ngModel)]="password"></mat-form-field><button mat-flat-button color="primary">进入平台</button></form></section>`,
  styles: [`.login{min-height:calc(100vh - 56px);display:grid;place-items:center}.panel{width:min(380px,92vw);display:grid;gap:12px}h1{margin:0 0 6px}`]
})
export class LoginComponent {
  username = 'admin';
  password = 'admin123456';
  constructor(private auth: AuthService, private router: Router) {}
  submit(): void { this.auth.login(this.username, this.password).subscribe(() => this.router.navigate(['/map'])); }
}
