import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { DashboardComponent } from './dashboard.component';
import { HoodsComponent } from './hoods/hoods.component';
import { AuthGuard } from '../core/auth/auth.guard';
import { BoardComponent } from './board/board.component';
import { TwitterCallbackComponent } from '../platforms/twitter/twitter-callback/twitter-callback.component';

const routes: Routes = [
  {
    path: '',
    component: DashboardComponent,
    children: [
      { path: '', component: HoodsComponent },
      { path: 'hoods/:id', component: BoardComponent },
      // Platform-specific Routes
      { path: 'twitter-callback', component: TwitterCallbackComponent },
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