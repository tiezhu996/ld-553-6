import { NgModule } from '@angular/core';
import { RouterModule } from '@angular/router';
import { SharedModule } from '../shared/shared.module';
import { LoginComponent } from './login/login.component';

@NgModule({ declarations: [LoginComponent], imports: [SharedModule, RouterModule.forChild([{ path: 'login', component: LoginComponent }, { path: '', redirectTo: 'login', pathMatch: 'full' }])] })
export class AuthModule {}
