import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { SharedModule } from './shared/shared.module';
import { HomepageComponent } from './homepage/homepage.component';
import { OrganizerspageComponent } from './organizerspage/organizerspage.component';
import { DashboardModule } from './dashboard/dashboard.module';
import { HoodpageComponent } from './hoodpage/hoodpage.component';
import { HoodspageComponent } from './hoodspage/hoodspage.component';
import { ApiModule } from './core/api/api.module';
import { HttpClientModule, HTTP_INTERCEPTORS } from '@angular/common/http';
import { BASE_PATH } from './core/api/variables';
import { environment } from 'src/environments/environment';
import { LoginComponent } from './login/login.component';
import { RegisterComponent } from './register/register.component';
import { ReactiveFormsModule } from '@angular/forms';
import { AuthTokenInterceptor } from './core/auth/auth-token.interceptor';

@NgModule({
  declarations: [
    AppComponent,
    HomepageComponent,
    OrganizerspageComponent,
    HoodpageComponent,
    HoodspageComponent,
    LoginComponent,
    RegisterComponent,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    SharedModule,
    DashboardModule,
    ApiModule,
    HttpClientModule,
    ReactiveFormsModule,
  ],
  providers: [
    { provide: BASE_PATH, useValue: environment.API_BASE_PATH },
    { provide: HTTP_INTERCEPTORS, useClass: AuthTokenInterceptor, multi: true },
  ],
  bootstrap: [AppComponent],
})
export class AppModule {}
