import { Component } from '@angular/core';
import { AuthService } from '../../shared/services/auth.service';

@Component({ standalone: false,
  selector: 'app-header',
  template: `<header class="top"><strong>TransitHub</strong><span>{{ auth.user()?.username || '未登录' }}</span><button mat-button (click)="auth.logout()">退出</button></header>`,
  styles: [`.top{height:56px;border-bottom:1px solid #d8e0d6;background:#fbfcf8;display:flex;align-items:center;gap:18px;padding:0 20px}.top strong{font-size:18px;margin-right:auto}`]
})
export class HeaderComponent { constructor(public auth: AuthService) {} }
