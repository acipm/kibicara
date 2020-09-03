import { Component, OnInit, Input } from '@angular/core';
import { TelegramService } from 'src/app/core/api';
import { TelegramBotInfoDialogComponent } from './telegram-bot-info-dialog/telegram-bot-info-dialog.component';
import { MatDialog } from '@angular/material/dialog';

@Component({
  selector: 'app-telegram-bot-card',
  templateUrl: './telegram-bot-card.component.html',
  styleUrls: ['./telegram-bot-card.component.scss'],
})
export class TelegramBotCardComponent implements OnInit {
  @Input() hoodId;
  telegrams$;

  constructor(
    private telegramService: TelegramService,
    private dialog: MatDialog
  ) {}

  ngOnInit(): void {
    this.telegrams$ = this.telegramService.getTelegramsPublic(this.hoodId);
  }

  onInfoClick() {
    this.dialog.open(TelegramBotInfoDialogComponent);
  }
}
