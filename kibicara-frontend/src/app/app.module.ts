import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { SharedModule } from './shared/shared.module';
import { HomepageComponent } from './homepage/homepage.component';
import { OrganizerspageComponent } from './organizerspage/organizerspage.component';
import { AuthModule } from './auth/auth.module';
import { DashboardModule } from './dashboard/dashboard.module';
import { HoodpageComponent } from './hoodpage/hoodpage.component';
import { HoodspageComponent } from './hoodspage/hoodspage.component';
import { ApiModule } from './api/api.module';


@NgModule({
  declarations: [
    AppComponent,
    HomepageComponent,
    OrganizerspageComponent,
    HoodpageComponent,
    HoodspageComponent,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    SharedModule,
    AuthModule,
    DashboardModule,
    ApiModule,
  ],
  providers: [],
  bootstrap: [AppComponent],
})
export class AppModule {}
