import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HoodsComponent } from './hoods/hoods.component';
import { SettingspageComponent } from './settingspage/settingspage.component';
import { DashboardComponent } from './dashboard.component';

@NgModule({
  declarations: [HoodsComponent, SettingspageComponent, DashboardComponent],
  imports: [CommonModule],
})
export class DashboardModule {}
