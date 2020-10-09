import { NgModule } from '@angular/core';
import { AuthRoutingModule } from './auth-routing.module';
import { ConfirmComponent } from './confirm/confirm.component';
import { RegisterComponent } from './register/register.component';
import { LoginComponent } from './login/login.component';
import { SharedModule } from '../shared/shared.module';
import { PasswordResetComponent } from './password-reset/password-reset.component';
import { SetPasswordComponent } from './password-reset/set-password/set-password.component';

@NgModule({
  declarations: [
    ConfirmComponent,
    LoginComponent,
    RegisterComponent,
    PasswordResetComponent,
    SetPasswordComponent,
  ],
  imports: [AuthRoutingModule, SharedModule],
})
export class AuthModule {}
