import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { AuthGuard } from './shared/guards/auth.guard';
import { RoleGuard } from './shared/guards/role.guard';

const routes: Routes = [
  { path: 'auth', loadChildren: () => import('./auth/auth.module').then(m => m.AuthModule) },
  { path: 'map', canActivate: [AuthGuard], loadChildren: () => import('./map/map.module').then(m => m.MapModule) },
  { path: 'vehicles', canActivate: [AuthGuard, RoleGuard], data: { roles: ['DRIVER', 'OPERATOR', 'ADMIN'] }, loadChildren: () => import('./vehicles/vehicles.module').then(m => m.VehiclesModule) },
  { path: 'charging', canActivate: [AuthGuard], loadChildren: () => import('./charging/charging.module').then(m => m.ChargingModule) },
  { path: 'orders', canActivate: [AuthGuard], loadChildren: () => import('./orders/orders.module').then(m => m.OrdersModule) },
  { path: 'dashboard', canActivate: [AuthGuard, RoleGuard], data: { roles: ['OPERATOR', 'ADMIN'] }, loadChildren: () => import('./dashboard/dashboard.module').then(m => m.DashboardModule) },
  { path: '', pathMatch: 'full', redirectTo: 'map' },
  { path: '**', redirectTo: 'map' }
];

@NgModule({ imports: [RouterModule.forRoot(routes)], exports: [RouterModule] })
export class AppRoutingModule {}
