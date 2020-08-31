import { Component, OnInit, Input } from '@angular/core';
import { Observable } from 'rxjs/internal/Observable';
import { EmailService, HoodsService } from 'src/app/core/api';
import { MatDialog } from '@angular/material/dialog';
import { EmailDialogComponent } from '../email-dialog/email-dialog.component';
import { EmailInfoDialogComponent } from '../email-info-dialog/email-info-dialog.component';
import { BotStatus } from '../../../core/model/status';
import { MatSnackBar } from '@angular/material/snack-bar';
import { environment } from 'src/environments/environment';

@Component({
  selector: 'app-email-settings',
  templateUrl: './email-settings.component.html',
  styleUrls: ['./email-settings.component.scss'],
})
export class EmailSettingsComponent implements OnInit {
  @Input() hoodId;
  emails$: Observable<Array<any>>;
  start = false;
  domain = environment.EMAIL_DOMAIN;

  constructor(
    private emailService: EmailService,
    public dialog: MatDialog,
    private snackBar: MatSnackBar
  ) {}

  ngOnInit(): void {
    this.reload();
  }

  private reload() {
    this.emails$ = this.emailService.getEmails(this.hoodId);
    this.emailService.statusEmail(this.hoodId).subscribe((status) => {
      if (status.status === BotStatus.RUNNING.toString()) {
        this.start = true;
      }
    });
  }

  onDelete(emailId) {
    this.emailService.deleteEmail(emailId, this.hoodId).subscribe(() => {
      this.reload();
    });
  }

  onCreate() {
    const dialogRef = this.dialog.open(EmailDialogComponent, {
      data: { hoodId: this.hoodId },
    });

    dialogRef.afterClosed().subscribe(() => {
      this.reload();
    });
  }

  onInfoClick() {
    this.dialog.open(EmailInfoDialogComponent);
  }

  onToggle() {
    if (this.start) {
      this.emailService.startEmail(this.hoodId).subscribe(
        () => {},
        (error) => {
          this.snackBar.open('Could not start. Check your settings.', 'Close', {
            duration: 2000,
          });
        }
      );
    } else {
      this.emailService.stopEmail(this.hoodId).subscribe(
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
