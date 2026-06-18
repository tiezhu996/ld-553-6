import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { MapMarker } from '../../shared/components/map-container/map-container.component';
import { TripOrder } from '../../shared/models/trip-order.model';
import { ApiService } from '../../shared/services/api.service';

@Component({ standalone: false,
  template: `<section class="page" *ngIf="order"><h1>{{ order.order_no }}</h1><div class="split"><app-map-container [markers]="markers" [path]="path"></app-map-container><aside class="panel"><p>{{ order.start_location }} → {{ order.end_location }}</p><p>{{ order.distance }} km · {{ order.duration }} 分钟 · ¥{{ order.fare }}</p><app-status-tag [value]="order.status"></app-status-tag></aside></div></section>`
})
export class OrderDetailComponent implements OnInit {
  order?: TripOrder;
  markers: MapMarker[] = [];
  path: Array<[number, number]> = [];
  constructor(private route: ActivatedRoute, private api: ApiService) {}
  ngOnInit(): void {
    const id = Number(this.route.snapshot.paramMap.get('id'));
    this.api.listOrders().subscribe(items => {
      this.order = items.find(o => o.id === id);
      if (this.order) {
        this.markers = [
          { lng: Number(this.order.start_lng), lat: Number(this.order.start_lat), label: '起点' },
          { lng: Number(this.order.end_lng), lat: Number(this.order.end_lat), label: '终点' }
        ];
        this.path = this.markers.map(m => [m.lng, m.lat]);
      }
    });
  }
}
