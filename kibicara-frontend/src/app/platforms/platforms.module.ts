import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { TelegramSettingsComponent } from './telegram/telegram-settings/telegram-settings.component';
import { SharedModule } from '../shared/shared.module';
import { TwitterSettingsComponent } from './twitter/twitter-settings/twitter-settings.component';
import { EmailSettingsComponent } from './email/email-settings/email-settings.component';
import { EmailDialogComponent } from './email/email-settings/email-dialog/email-dialog.component';
import { EmailInfoDialogComponent } from './email/email-settings/email-info-dialog/email-info-dialog.component';
import { TelegramInfoDialogComponent } from './telegram/telegram-info-dialog/telegram-info-dialog.component';
import { TelegramDialogComponent } from './telegram/telegram-dialog/telegram-dialog.component';
import { TwitterInfoDialogComponent } from './twitter/twitter-info-dialog/twitter-info-dialog.component';
import { TwitterCallbackComponent } from './twitter/twitter-callback/twitter-callback.component';
import { TwitterCorpsesPipe } from './twitter/twitter-corpses-pipe/twitter-corpses.pipe';
import { PlatformsInfoPageComponent } from './platforms-info-page/platforms-info-page.component';
import { EmailBotCardComponent } from './email/email-bot-card/email-bot-card.component';
import { TelegramBotCardComponent } from './telegram/telegram-bot-card/telegram-bot-card.component';
import { TwitterBotCardComponent } from './twitter/twitter-bot-card/twitter-bot-card.component';
import { PlatformsInfoDialogComponent } from './platforms-info-page/platforms-info-dialog/platforms-info-dialog.component';
import { EmailBotInfoDialogComponent } from './email/email-bot-card/email-bot-info-dialog/email-bot-info-dialog.component';
import { TelegramBotInfoDialogComponent } from './telegram/telegram-bot-card/telegram-bot-info-dialog/telegram-bot-info-dialog.component';
import { TwitterBotInfoDialogComponent } from './twitter/twitter-bot-card/twitter-bot-info-dialog/twitter-bot-info-dialog.component';
import { EmailConfirmationComponent } from './email/email-confirmation/email-confirmation.component';
import { EmailUnsubscribeComponent } from './email/email-unsubscribe/email-unsubscribe.component';

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
    TwitterCorpsesPipe,
    PlatformsInfoPageComponent,
    EmailBotCardComponent,
    TelegramBotCardComponent,
    TwitterBotCardComponent,
    PlatformsInfoDialogComponent,
    EmailBotInfoDialogComponent,
    TelegramBotInfoDialogComponent,
    TwitterBotInfoDialogComponent,
    EmailConfirmationComponent,
    EmailUnsubscribeComponent,
  ],
  imports: [CommonModule, SharedModule],
  exports: [
    TelegramSettingsComponent,
    TwitterSettingsComponent,
    EmailSettingsComponent,
    PlatformsInfoPageComponent,
  ],
})
export class PlatformsModule {}
