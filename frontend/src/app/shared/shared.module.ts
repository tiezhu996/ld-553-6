import { CommonModule } from '@angular/common';
import { NgModule } from '@angular/core';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatIconModule } from '@angular/material/icon';
import { MatInputModule } from '@angular/material/input';
import { MatSelectModule } from '@angular/material/select';
import { MatSnackBarModule } from '@angular/material/snack-bar';
import { MatTableModule } from '@angular/material/table';
import { HasRoleDirective } from './directives/has-role.directive';
import { MapContainerComponent } from './components/map-container/map-container.component';
import { StatsCardComponent } from './components/stats-card/stats-card.component';
import { StatusTagComponent } from './components/status-tag/status-tag.component';
import { StatusTranslatePipe } from './pipes/status-translate.pipe';

@NgModule({
  declarations: [HasRoleDirective, MapContainerComponent, StatsCardComponent, StatusTagComponent, StatusTranslatePipe],
  imports: [CommonModule, FormsModule, ReactiveFormsModule, MatButtonModule, MatCardModule, MatFormFieldModule, MatIconModule, MatInputModule, MatSelectModule, MatSnackBarModule, MatTableModule],
  exports: [CommonModule, FormsModule, ReactiveFormsModule, MatButtonModule, MatCardModule, MatFormFieldModule, MatIconModule, MatInputModule, MatSelectModule, MatSnackBarModule, MatTableModule, HasRoleDirective, MapContainerComponent, StatsCardComponent, StatusTagComponent, StatusTranslatePipe]
})
export class SharedModule {}
