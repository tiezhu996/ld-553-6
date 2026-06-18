import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { MaintenanceRecord } from '../../shared/models/maintenance-record.model';
import { Vehicle } from '../../shared/models/vehicle.model';
import { ApiService } from '../../shared/services/api.service';

@Component({ standalone: false,
  template: `<section class="page"><a routerLink="/vehicles">返回车辆</a><div class="panel" *ngIf="vehicle"><h1>{{ vehicle.plate_number }}</h1><p>{{ vehicle.brand }} {{ vehicle.model }} · {{ vehicle.year }}</p><app-status-tag [value]="vehicle.status"></app-status-tag></div><h2>维修记录</h2><div class="table-wrap"><table><tr><th>类型</th><th>费用</th><th>开始</th><th>结束</th><th>状态</th></tr><tr *ngFor="let r of records"><td>{{ r.type }}</td><td>{{ r.cost }}</td><td>{{ r.start_date }}</td><td>{{ r.end_date || '-' }}</td><td>{{ r.status }}</td></tr></table></div></section>`
})
export class VehicleDetailComponent implements OnInit {
  vehicle?: Vehicle;
  records: MaintenanceRecord[] = [];
  constructor(private route: ActivatedRoute, private api: ApiService) {}
  ngOnInit(): void {
    const id = Number(this.route.snapshot.paramMap.get('id'));
    this.api.listVehicles().subscribe(items => this.vehicle = items.find(v => v.id === id));
    this.api.vehicleMaintenance(id).subscribe(records => this.records = records);
  }
}
