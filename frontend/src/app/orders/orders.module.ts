import { NgModule } from '@angular/core';
import { RouterModule } from '@angular/router';
import { SharedModule } from '../shared/shared.module';
import { OrderDetailComponent } from './order-detail/order-detail.component';
import { OrderListComponent } from './order-list/order-list.component';

@NgModule({ declarations: [OrderListComponent, OrderDetailComponent], imports: [SharedModule, RouterModule.forChild([{ path: '', component: OrderListComponent }, { path: ':id', component: OrderDetailComponent }])] })
export class OrdersModule {}
