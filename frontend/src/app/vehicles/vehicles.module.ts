import { NgModule } from '@angular/core';
import { RouterModule } from '@angular/router';
import { SharedModule } from '../shared/shared.module';
import { VehicleDetailComponent } from './vehicle-detail/vehicle-detail.component';
import { VehicleFormComponent } from './vehicle-form/vehicle-form.component';
import { VehicleListComponent } from './vehicle-list/vehicle-list.component';

@NgModule({ declarations: [VehicleListComponent, VehicleDetailComponent, VehicleFormComponent], imports: [SharedModule, RouterModule.forChild([{ path: '', component: VehicleListComponent }, { path: 'new', component: VehicleFormComponent }, { path: ':id', component: VehicleDetailComponent }])] })
export class VehiclesModule {}
