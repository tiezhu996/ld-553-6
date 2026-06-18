import { Component, OnInit } from '@angular/core';
import { forkJoin } from 'rxjs';
import { PileStatus, VehicleStatus, VehicleType } from '../shared/constants/enums';
import { MapMarker } from '../shared/components/map-container/map-container.component';
import { ApiService } from '../shared/services/api.service';

@Component({ standalone: false,
  template: `<section class="map-page"><app-map-container [markers]="markers"></app-map-container><aside class="floating panel"><h2>实时总览</h2><div class="metric"><b>{{ vehicleCount }}</b><span>运营车辆</span></div><div class="metric"><b>{{ pileCount }}</b><span>充电桩</span></div><label>车辆类型<select [(ngModel)]="vehicleType"><option value="">全部</option><option *ngFor="let t of vehicleTypes" [value]="t">{{ t }}</option></select></label><label>状态<select [(ngModel)]="status"><option value="">全部</option><option *ngFor="let s of statuses" [value]="s">{{ s | statusTranslate }}</option></select></label></aside><div class="legend panel"><span>绿 空闲/运营</span><span>蓝 充电中</span><span>红 故障</span></div></section>`,
  styles: [`.map-page{position:relative;height:calc(100vh - 56px);padding:16px;box-sizing:border-box}.map-page app-map-container{display:block;height:100%}.floating{position:absolute;left:32px;top:32px;width:240px}.metric{display:flex;align-items:baseline;gap:8px;margin:10px 0}.metric b{font-size:30px}.floating label{display:grid;margin-top:12px;color:#5f6f67}.floating select{margin-top:6px;padding:7px}.legend{position:absolute;right:32px;bottom:32px;display:flex;gap:12px}`]
})
export class MapPageComponent implements OnInit {
  markers: MapMarker[] = [];
  vehicleCount = 0;
  pileCount = 0;
  vehicleType = '';
  status = '';
  vehicleTypes = Object.values(VehicleType);
  statuses = [...Object.values(VehicleStatus), ...Object.values(PileStatus)];
  constructor(private api: ApiService) {}
  ngOnInit(): void {
    forkJoin([this.api.vehicleLocations(), this.api.pileLocations()]).subscribe(([vehicles, piles]) => {
      this.vehicleCount = vehicles.length;
      this.pileCount = piles.length;
      this.markers = [
        ...vehicles.map(v => ({ lng: Number(v.lng), lat: Number(v.lat), label: v.plate_number, status: v.status, kind: 'vehicle' as const })),
        ...piles.map(p => ({ lng: Number(p.lng), lat: Number(p.lat), label: p.code, status: p.status, kind: 'pile' as const }))
      ];
    });
  }
}
