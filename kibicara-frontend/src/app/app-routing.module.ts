import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { NotFoundComponent } from './shared/not-found/not-found.component';
import { HomepageComponent } from './homepage/homepage.component';
import { LoginComponent } from './auth/login/login.component';
import { RegisterComponent } from './auth/register/register.component';
import { OrganizerspageComponent } from './organizerspage/organizerspage.component';
import { HoodspageComponent } from './hoodspage/hoodspage.component';
import { HoodpageComponent } from './hoodpage/hoodpage.component';
import { SharedModule } from './shared/shared.module';
import { ConfirmComponent } from './auth/confirm/confirm.component';
import { EmailConfirmationComponent } from './platforms/email/email-confirmation/email-confirmation.component';
import { EmailUnsubscribeComponent } from './platforms/email/email-unsubscribe/email-unsubscribe.component';

const routes: Routes = [
  { path: '', component: HomepageComponent },
  { path: 'login', component: LoginComponent },
  { path: 'register', component: RegisterComponent },
  { path: 'confirm', component: ConfirmComponent },
  { path: 'organizers', component: OrganizerspageComponent },
  { path: 'hoods', component: HoodspageComponent },
  { path: 'hoods/:id', component: HoodpageComponent },
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
