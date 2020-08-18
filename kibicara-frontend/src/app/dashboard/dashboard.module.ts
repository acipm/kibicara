import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HoodsComponent } from './hoods/hoods.component';
import { SettingspageComponent } from './settingspage/settingspage.component';
import { DashboardComponent } from './dashboard.component';
import { DashboardRoutingModule } from './dashboard-routing.module';

@NgModule({
  declarations: [HoodsComponent, SettingspageComponent, DashboardComponent],
  imports: [CommonModule, DashboardRoutingModule],
})
export class DashboardModule {}
