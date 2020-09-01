import { Component, OnInit, Input } from '@angular/core';
import { TelegramService } from 'src/app/core/api';
import { Observer, Observable } from 'rxjs';
import { TelegramInfoDialogComponent } from '../telegram-info-dialog/telegram-info-dialog.component';
import { MatDialog } from '@angular/material/dialog';
import { TelegramDialogComponent } from '../telegram-dialog/telegram-dialog.component';
import { YesNoDialogComponent } from 'src/app/shared/yes-no-dialog/yes-no-dialog.component';

@Component({
  selector: 'app-telegram-settings',
  templateUrl: './telegram-settings.component.html',
  styleUrls: ['./telegram-settings.component.scss'],
})
export class TelegramSettingsComponent implements OnInit {
  @Input() hoodId;
  telegrams$: Observable<Array<any>>;

  constructor(
    private telegramService: TelegramService,
    public dialog: MatDialog
  ) {}

  ngOnInit(): void {
    this.reload();
  }

  private reload() {
    this.telegrams$ = this.telegramService.getTelegrams(this.hoodId);
  }

  onInfoClick() {
    this.dialog.open(TelegramInfoDialogComponent);
  }

  onDelete(telegramId) {
    const dialogRef = this.dialog.open(YesNoDialogComponent, {
      data: {
        title: 'Warning',
        content:
          'This will also delete the list of subscribers of the telegram bot.',
      },
    });

    dialogRef.afterClosed().subscribe((response) => {
      if (response) {
        this.telegramService
          .deleteTelegram(telegramId, this.hoodId)
          .subscribe(() => {
            this.reload();
          });
      }
    });
  }

  onCreate() {
    const dialogRef = this.dialog.open(TelegramDialogComponent, {
      data: { hoodId: this.hoodId },
    });

    dialogRef.afterClosed().subscribe(() => {
      this.reload();
    });
  }

  onEdit(telegramId) {
    const dialogRef = this.dialog.open(TelegramDialogComponent, {
      data: { hoodId: this.hoodId, telegramId: telegramId },
    });

    dialogRef.afterClosed().subscribe(() => {
      this.reload();
    });
  }
}
