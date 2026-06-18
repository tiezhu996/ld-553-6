import { NgModule } from '@angular/core';
import { RouterModule } from '@angular/router';
import { SharedModule } from '../shared/shared.module';
import { MapPageComponent } from './map-page.component';

@NgModule({ declarations: [MapPageComponent], imports: [SharedModule, RouterModule.forChild([{ path: '', component: MapPageComponent }])] })
export class MapModule {}
