import { Component, OnInit } from '@angular/core';
import { VehicleStatus, VehicleType } from '../../shared/constants/enums';
import { Vehicle } from '../../shared/models/vehicle.model';
import { ApiService } from '../../shared/services/api.service';

@Component({ standalone: false,
  template: `<section class="page"><h1>车辆管理</h1><div class="toolbar"><mat-form-field><mat-label>类型</mat-label><mat-select [(ngModel)]="type" (selectionChange)="load()"><mat-option value="">全部</mat-option><mat-option *ngFor="let t of vehicleTypes" [value]="t">{{ t }}</mat-option></mat-select></mat-form-field><mat-form-field><mat-label>状态</mat-label><mat-select [(ngModel)]="status" (selectionChange)="load()"><mat-option value="">全部</mat-option><mat-option *ngFor="let s of statuses" [value]="s">{{ s | statusTranslate }}</mat-option></mat-select></mat-form-field><button mat-flat-button color="primary" *appHasRole="['OPERATOR','ADMIN']">注册车辆</button></div><div class="table-wrap"><table><thead><tr><th>车牌</th><th>类型</th><th>车型</th><th>司机</th><th>保险到期</th><th>状态</th><th>操作</th></tr></thead><tbody><tr *ngFor="let v of vehicles"><td><a [routerLink]="['/vehicles', v.id]">{{ v.plate_number }}</a></td><td>{{ v.type }}</td><td>{{ v.brand }} {{ v.model }}</td><td>{{ v.driver_detail?.username || '-' }}</td><td>{{ v.insurance_expiry }}</td><td><app-status-tag [value]="v.status"></app-status-tag></td><td><button mat-button *appHasRole="['OPERATOR','ADMIN']">审核/调度</button></td></tr></tbody></table></div></section>`
})
export class VehicleListComponent implements OnInit {
  vehicles: Vehicle[] = [];
  type = '';
  status = '';
  vehicleTypes = Object.values(VehicleType);
  statuses = Object.values(VehicleStatus);
  constructor(private api: ApiService) {}
  ngOnInit(): void { this.load(); }
  load(): void { this.api.listVehicles({ type: this.type, status: this.status }).subscribe(v => this.vehicles = v); }
}
