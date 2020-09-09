import { NgModule } from '@angular/core';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { SharedModule } from './shared/shared.module';
import { DashboardModule } from './dashboard/dashboard.module';
import { ApiModule } from './core/api/api.module';
import { HttpClientModule, HTTP_INTERCEPTORS } from '@angular/common/http';
import { BASE_PATH } from './core/api/variables';
import { environment } from 'src/environments/environment';
import { AuthTokenInterceptor } from './core/auth/auth-token.interceptor';
import { ErrorInterceptor } from './core/auth/error.interceptor';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { PublicPagesModule } from './public-pages/public-pages.module';
import { AuthModule } from './auth/auth.module';

@NgModule({
  declarations: [AppComponent],
  imports: [
    AppRoutingModule,
    SharedModule,
    DashboardModule,
    PublicPagesModule,
    AuthModule,
    ApiModule,
    HttpClientModule,
    BrowserAnimationsModule,
  ],
  providers: [
    { provide: BASE_PATH, useValue: environment.API_BASE_PATH },
    { provide: HTTP_INTERCEPTORS, useClass: AuthTokenInterceptor, multi: true },
    { provide: HTTP_INTERCEPTORS, useClass: ErrorInterceptor, multi: true },
  ],
  bootstrap: [AppComponent],
})
export class AppModule {}
