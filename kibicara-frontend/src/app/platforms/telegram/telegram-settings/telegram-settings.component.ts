import { Component, OnInit, Input } from '@angular/core';
import { TelegramService } from 'src/app/core/api';
import { Observable } from 'rxjs';
import { TelegramInfoDialogComponent } from '../telegram-info-dialog/telegram-info-dialog.component';
import { MatDialog } from '@angular/material/dialog';
import { TelegramDialogComponent } from '../telegram-dialog/telegram-dialog.component';
import { YesNoDialogComponent } from 'src/app/shared/yes-no-dialog/yes-no-dialog.component';
import { MatSnackBar } from '@angular/material/snack-bar';

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
    public dialog: MatDialog,
    private snackBar: MatSnackBar
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

  onChange(telegram) {
    if (telegram.enabled === 0) {
      this.telegramService.startTelegram(telegram.id, this.hoodId).subscribe(
        () => {},
        (error) => {
          this.snackBar.open('Could not start. Check your settings.', 'Close', {
            duration: 2000,
          });
        }
      );
    } else if (telegram.enabled === 1) {
      this.telegramService.stopTelegram(telegram.id, this.hoodId).subscribe(
        () => {},
        (error) => {
          this.snackBar.open('Could not stop. Check your settings.', 'Close', {
            duration: 2000,
          });
        }
      );
    }
    // TODO yeah i know this is bad, implement disabling/enabling
    setTimeout(() => {
      this.reload();
    }, 100);
  }
}
