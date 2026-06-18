import { NgModule } from '@angular/core';
import { RouterModule } from '@angular/router';
import { SharedModule } from '../shared/shared.module';
import { ChargingDetailComponent } from './charging-detail/charging-detail.component';
import { ChargingListComponent } from './charging-list/charging-list.component';

@NgModule({ declarations: [ChargingListComponent, ChargingDetailComponent], imports: [SharedModule, RouterModule.forChild([{ path: '', component: ChargingListComponent }, { path: ':id', component: ChargingDetailComponent }])] })
export class ChargingModule {}
