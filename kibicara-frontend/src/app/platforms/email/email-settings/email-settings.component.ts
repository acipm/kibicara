import { Component, OnInit, Input } from '@angular/core';
import { Observable } from 'rxjs/internal/Observable';
import { EmailService } from 'src/app/core/api';
import { MatDialog } from '@angular/material/dialog';
import { Router } from '@angular/router';
import { EmailDialogComponent } from '../email-dialog/email-dialog.component';

@Component({
  selector: 'app-email-settings',
  templateUrl: './email-settings.component.html',
  styleUrls: ['./email-settings.component.scss'],
})
export class EmailSettingsComponent implements OnInit {
  @Input() hoodId;
  emails$: Observable<Array<any>>;

  constructor(
    private emailService: EmailService,
    public dialog: MatDialog,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.reload();
  }

  private reload() {
    this.emails$ = this.emailService.getEmails(this.hoodId);
  }

  onDelete(emailId) {
    this.emailService.deleteEmail(emailId, this.hoodId).subscribe(() => {
      this.reload();
    });
  }

  onCreate() {
    const dialogRef = this.dialog.open(EmailDialogComponent);

    dialogRef.afterClosed().subscribe((hood) => {
      // if (hood && hood.id) {
      //   this.router.navigate(['/dashboard/hoods', hood.id]);
      // }
    });
  }
}
