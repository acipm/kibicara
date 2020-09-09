import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { NotFoundComponent } from './shared/not-found/not-found.component';
import { SharedModule } from './shared/shared.module';
import { EmailConfirmationComponent } from './platforms/email/email-confirmation/email-confirmation.component';
import { EmailUnsubscribeComponent } from './platforms/email/email-unsubscribe/email-unsubscribe.component';

const routes: Routes = [
  {
    path: '',
    loadChildren: () =>
      import('./public-pages/public-pages.module').then(
        (m) => m.PublicPagesModule
      ),
  },
  {
    path: '',
    loadChildren: () => import('./auth/auth.module').then((m) => m.AuthModule),
  },
  { path: 'hoods/:id/email-confirm', component: EmailConfirmationComponent },
  { path: 'hoods/:id/email-unsubscribe', component: EmailUnsubscribeComponent },
  {
    path: 'dashboard',
    loadChildren: () =>
      import('./dashboard/dashboard.module').then((m) => m.DashboardModule),
  },
  { path: '**', component: NotFoundComponent },
];

@NgModule({
  imports: [RouterModule.forRoot(routes), SharedModule],
  exports: [RouterModule],
})
export class AppRoutingModule {}
