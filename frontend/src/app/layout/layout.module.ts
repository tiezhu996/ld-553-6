import { NgModule } from '@angular/core';
import { RouterModule } from '@angular/router';
import { SharedModule } from '../shared/shared.module';
import { HeaderComponent } from './header/header.component';
import { LayoutComponent } from './layout.component';
import { SidebarComponent } from './sidebar/sidebar.component';

@NgModule({ declarations: [HeaderComponent, SidebarComponent, LayoutComponent], imports: [SharedModule, RouterModule], exports: [LayoutComponent] })
export class LayoutModule {}
