import { Component, OnInit } from '@angular/core';
import { DashboardOverview } from '../shared/models/dashboard.model';
import { ApiService } from '../shared/services/api.service';

@Component({ standalone: false,
  template: `<section class="page"><h1>运营大屏</h1><div class="grid grid-4" *ngIf="overview"><app-stats-card title="实时车辆" [value]="overview.vehicles_online + '/' + overview.vehicles_total" trend="在线 / 总数"></app-stats-card><app-stats-card title="今日订单" [value]="overview.today_orders"></app-stats-card><app-stats-card title="今日收入" [value]="'¥' + overview.today_revenue"></app-stats-card><app-stats-card title="充电桩利用率" [value]="overview.pile_utilization + '%'"></app-stats-card></div><div class="grid charts"><section class="panel"><h2>订单趋势</h2><div class="bars"><span *ngFor="let item of trend" [style.height.px]="20 + item.count * 8">{{ item.count }}</span></div></section><section class="panel"><h2>收入统计</h2><pre>{{ revenue | json }}</pre></section><section class="panel"><h2>车辆类型分布</h2><pre>{{ revenue?.vehicle_distribution | json }}</pre></section><section class="panel"><h2>充电桩利用率</h2><strong>{{ overview?.pile_utilization || 0 }}%</strong></section></div></section>`,
  styles: [`.charts{grid-template-columns:repeat(2,minmax(0,1fr));margin-top:18px}.bars{height:180px;display:flex;align-items:flex-end;gap:10px}.bars span{width:32px;background:#0e7c59;color:#fff;text-align:center;border-radius:4px 4px 0 0}@media(max-width:900px){.charts{grid-template-columns:1fr}}`]
})
export class DashboardComponent implements OnInit {
  overview?: DashboardOverview;
  trend: Array<{ day: string; count: number }> = [];
  revenue: any;
  constructor(private api: ApiService) {}
  ngOnInit(): void {
    this.api.dashboardOverview().subscribe(v => this.overview = v);
    this.api.orderTrend().subscribe(v => this.trend = v);
    this.api.revenueStats().subscribe(v => this.revenue = v);
  }
}
