import { Component, OnInit } from '@angular/core';
import { OrderStatus } from '../../shared/constants/enums';
import { TripOrder } from '../../shared/models/trip-order.model';
import { ApiService } from '../../shared/services/api.service';

@Component({ standalone: false,
  template: `<section class="page"><h1>出行订单</h1><div class="toolbar"><mat-form-field><mat-label>状态</mat-label><mat-select [(ngModel)]="status" (selectionChange)="load()"><mat-option value="">全部</mat-option><mat-option *ngFor="let s of statuses" [value]="s">{{ s | statusTranslate }}</mat-option></mat-select></mat-form-field></div><div class="table-wrap"><table><thead><tr><th>订单号</th><th>路线</th><th>车辆</th><th>距离</th><th>费用</th><th>订单状态</th><th>支付</th></tr></thead><tbody><tr *ngFor="let o of orders"><td><a [routerLink]="['/orders', o.id]">{{ o.order_no }}</a></td><td>{{ o.start_location }} → {{ o.end_location }}</td><td>{{ o.vehicle_detail?.plate_number || '-' }}</td><td>{{ o.distance }} km</td><td>¥{{ o.fare }}</td><td><app-status-tag [value]="o.status"></app-status-tag></td><td><app-status-tag [value]="o.payment_status"></app-status-tag></td></tr></tbody></table></div></section>`
})
export class OrderListComponent implements OnInit {
  orders: TripOrder[] = [];
  status = '';
  statuses = Object.values(OrderStatus);
  constructor(private api: ApiService) {}
  ngOnInit(): void { this.load(); }
  load(): void { this.api.listOrders({ status: this.status }).subscribe(orders => this.orders = orders); }
}
