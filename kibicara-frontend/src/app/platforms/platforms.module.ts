import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { TelegramSettingsComponent } from './telegram/telegram-settings/telegram-settings.component';
import { SharedModule } from '../shared/shared.module';
import { TwitterSettingsComponent } from './twitter/twitter-settings/twitter-settings.component';
import { EmailSettingsComponent } from './email/email-settings/email-settings.component';

@NgModule({
  declarations: [
    TelegramSettingsComponent,
    TwitterSettingsComponent,
    EmailSettingsComponent,
  ],
  imports: [CommonModule, SharedModule],
  exports: [
    TelegramSettingsComponent,
    TwitterSettingsComponent,
    EmailSettingsComponent,
  ],
})
export class PlatformsModule {}
