import { AfterViewInit, Component, ElementRef, Input, ViewChild } from '@angular/core';
import { MapService } from '../../services/map.service';

export interface MapMarker { lng: number; lat: number; label: string; status?: string; kind?: 'vehicle' | 'pile'; }

@Component({ standalone: false,
  selector: 'app-map-container',
  template: `<div class="map-host" #host><div *ngIf="fallback" class="fallback"><strong>TransitHub 地图</strong><span>高德地图 Key 未配置或网络不可用，显示坐标清单。</span><p *ngFor="let marker of markers">{{ marker.label }} · {{ marker.lng }}, {{ marker.lat }}</p></div></div>`,
  styles: [`.map-host{height:100%;min-height:420px;border:1px solid #d8e0d6;border-radius:8px;overflow:hidden;background:#eaf0e7}.fallback{padding:22px;color:#12201b}.fallback span{display:block;margin:8px 0 14px;color:#5f6f67}`]
})
export class MapContainerComponent implements AfterViewInit {
  @Input() markers: MapMarker[] = [];
  @Input() path: Array<[number, number]> = [];
  @ViewChild('host', { static: true }) host!: ElementRef<HTMLElement>;
  fallback = false;
  constructor(private mapService: MapService) {}
  async ngAfterViewInit(): Promise<void> {
    try {
      await this.mapService.load();
      const map = this.mapService.createMap(this.host.nativeElement);
      const AMapRef = (window as any).AMap;
      this.markers.forEach(marker => new AMapRef.Marker({ map, position: [marker.lng, marker.lat], label: { content: marker.label } }));
      if (this.path.length) new AMapRef.Polyline({ map, path: this.path, strokeColor: '#0e7c59', strokeWeight: 5 });
    } catch {
      this.fallback = true;
    }
  }
}
