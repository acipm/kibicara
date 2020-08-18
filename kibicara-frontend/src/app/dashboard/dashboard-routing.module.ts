import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { DashboardComponent } from './dashboard.component';
import { HoodsComponent } from './hoods/hoods.component';
import { SettingspageComponent } from './settingspage/settingspage.component';
import { AuthGuard } from '../core/auth/auth.guard';

const routes: Routes = [
  {
    path: '',
    component: DashboardComponent,
    children: [
      { path: '', component: HoodsComponent },
      { path: 'settings', component: SettingspageComponent },
    ],
    canActivate: [AuthGuard],
  },
];

@NgModule({
  declarations: [],
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule],
})
export class DashboardRoutingModule {}
