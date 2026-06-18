import { Component } from '@angular/core';
import { AuthService } from '../../shared/services/auth.service';

@Component({ standalone: false,
  selector: 'app-sidebar',
  template: `<nav class="side"><ng-container *ngFor="let item of items"><a *appHasRole="item.roles" [routerLink]="item.path" routerLinkActive="active">{{ item.label }}</a></ng-container></nav>`,
  styles: [`.side{width:188px;background:#12201b;color:#eef4eb;min-height:calc(100vh - 56px);padding:18px 10px;box-sizing:border-box}.side a{display:block;color:#dce7dc;text-decoration:none;padding:11px 12px;border-radius:6px;margin-bottom:4px}.side a.active,.side a:hover{background:#274139;color:#fff}`]
})
export class SidebarComponent {
  items = [
    { label: '地图总览', path: '/map', roles: ['DRIVER', 'OPERATOR', 'ADMIN'] },
    { label: '车辆管理', path: '/vehicles', roles: ['DRIVER', 'OPERATOR', 'ADMIN'] },
    { label: '充电桩', path: '/charging', roles: ['DRIVER', 'OPERATOR', 'ADMIN'] },
    { label: '出行订单', path: '/orders', roles: ['DRIVER', 'OPERATOR', 'ADMIN'] },
    { label: '运营大屏', path: '/dashboard', roles: ['OPERATOR', 'ADMIN'] }
  ] as any[];
  constructor(public auth: AuthService) {}
}
