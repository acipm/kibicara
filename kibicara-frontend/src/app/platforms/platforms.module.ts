import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { TelegramSettingsComponent } from './telegram/telegram-settings/telegram-settings.component';
import { SharedModule } from '../shared/shared.module';
import { TwitterSettingsComponent } from './twitter/twitter-settings/twitter-settings.component';
import { EmailSettingsComponent } from './email/email-settings/email-settings.component';
import { EmailDialogComponent } from './email/email-dialog/email-dialog.component';
import { EmailInfoDialogComponent } from './email/email-info-dialog/email-info-dialog.component';
import { TelegramInfoDialogComponent } from './telegram/telegram-info-dialog/telegram-info-dialog.component';
import { TelegramDialogComponent } from './telegram/telegram-dialog/telegram-dialog.component';
import { TwitterInfoDialogComponent } from './twitter/twitter-info-dialog/twitter-info-dialog.component';
import { TwitterCallbackComponent } from './twitter/twitter-callback/twitter-callback.component';

@NgModule({
  declarations: [
    TelegramSettingsComponent,
    TwitterSettingsComponent,
    EmailSettingsComponent,
    EmailDialogComponent,
    EmailInfoDialogComponent,
    TelegramInfoDialogComponent,
    TelegramDialogComponent,
    TwitterInfoDialogComponent,
    TwitterCallbackComponent,
  ],
  imports: [CommonModule, SharedModule],
  exports: [
    TelegramSettingsComponent,
    TwitterSettingsComponent,
    EmailSettingsComponent,
  ],
})
export class PlatformsModule {}
