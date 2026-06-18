import { Component, OnInit } from '@angular/core';
import { PileStatus, PileType } from '../../shared/constants/enums';
import { MapMarker } from '../../shared/components/map-container/map-container.component';
import { ChargingPile } from '../../shared/models/charging-pile.model';
import { ApiService } from '../../shared/services/api.service';

@Component({ standalone: false,
  template: `<section class="page"><h1>充电桩管理</h1><div class="toolbar"><mat-form-field><mat-label>类型</mat-label><mat-select [(ngModel)]="type" (selectionChange)="load()"><mat-option value="">全部</mat-option><mat-option *ngFor="let t of types" [value]="t">{{ t }}</mat-option></mat-select></mat-form-field><mat-form-field><mat-label>状态</mat-label><mat-select [(ngModel)]="status" (selectionChange)="load()"><mat-option value="">全部</mat-option><mat-option *ngFor="let s of statuses" [value]="s">{{ s | statusTranslate }}</mat-option></mat-select></mat-form-field></div><div class="split"><app-map-container [markers]="markers"></app-map-container><aside class="panel"><h2>桩位列表</h2><article class="pile" *ngFor="let p of piles" [class.fault]="p.status==='FAULTY'"><b>{{ p.code }}</b><span>{{ p.location }}</span><app-status-tag [value]="p.status"></app-status-tag><small>{{ p.power }}kW · ¥{{ p.price_per_kwh }}/kWh</small><button mat-button *appHasRole="['OPERATOR','ADMIN']" (click)="markFault(p)">故障报修</button></article></aside></div></section>`,
  styles: [`.pile{display:grid;gap:6px;border-bottom:1px solid #d8e0d6;padding:12px 0}.pile small,.pile span{color:#5f6f67}.fault{animation:pulse 1s infinite}@keyframes pulse{50%{background:#f8e6e1}}`]
})
export class ChargingListComponent implements OnInit {
  piles: ChargingPile[] = [];
  markers: MapMarker[] = [];
  type = '';
  status = '';
  types = Object.values(PileType);
  statuses = Object.values(PileStatus);
  constructor(private api: ApiService) {}
  ngOnInit(): void { this.load(); }
  load(): void {
    this.api.listPiles({ type: this.type, status: this.status }).subscribe(piles => {
      this.piles = piles;
      this.markers = piles.map(p => ({ lng: Number(p.lng), lat: Number(p.lat), label: p.code, status: p.status, kind: 'pile' }));
    });
  }
  markFault(pile: ChargingPile): void { this.api.patchPileStatus(pile.id, PileStatus.FAULTY).subscribe(() => this.load()); }
}
