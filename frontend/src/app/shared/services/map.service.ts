import { Injectable } from '@angular/core';
import { environment } from '../../../environments/environment';

declare const AMap: any;

@Injectable({ providedIn: 'root' })
export class MapService {
  load(): Promise<void> {
    if ((window as any).AMap) return Promise.resolve();
    return new Promise((resolve, reject) => {
      const script = document.createElement('script');
      script.src = `https://webapi.amap.com/maps?v=2.0&key=${environment.amapApiKey}`;
      script.onload = () => resolve();
      script.onerror = () => reject(new Error('高德地图加载失败'));
      document.body.appendChild(script);
    });
  }

  createMap(el: HTMLElement, center: [number, number] = [121.4737, 31.2304]): any {
    return new AMap.Map(el, { center, zoom: 12, viewMode: '2D' });
  }
}
