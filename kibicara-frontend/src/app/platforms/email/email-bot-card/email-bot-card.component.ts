import { Component, OnInit, Input } from '@angular/core';
import { EmailService } from 'src/app/core/api';
import { environment } from 'src/environments/environment';
import { FormGroup, FormBuilder, Validators } from '@angular/forms';
import { EmailBotInfoDialogComponent } from './email-bot-info-dialog/email-bot-info-dialog.component';
import { MatDialog } from '@angular/material/dialog';
import { first } from 'rxjs/operators';
import { MatSnackBar } from '@angular/material/snack-bar';

@Component({
  selector: 'app-email-bot-card',
  templateUrl: './email-bot-card.component.html',
  styleUrls: ['./email-bot-card.component.scss'],
})
export class EmailBotCardComponent implements OnInit {
  @Input() hoodId;
  emails$;
  emailDomain = environment.EMAIL_DOMAIN;
  form: FormGroup;

  constructor(
    private emailService: EmailService,
    private formBuilder: FormBuilder,
    private dialog: MatDialog,
    private snackBar: MatSnackBar
  ) {}

  ngOnInit(): void {
    this.emails$ = this.emailService.getEmailsPublic(this.hoodId);
    this.form = this.formBuilder.group({
      email: ['', Validators.required],
    });
  }

  onInfoClick() {
    this.dialog.open(EmailBotInfoDialogComponent);
  }

  onSubmit() {
    if (this.form.invalid) {
      return;
    }

    this.emailService
      .subscribe(this.hoodId, {
        email: this.form.controls.email.value,
      })
      .pipe(first())
      .subscribe(
        (data) => {
          this.form.reset();
          this.snackBar.open(
            'Successful! Check your e-mail inbox to confirm your subscription.',
            'Close',
            {
              duration: 2000,
            }
          );
        },
        (error) => {
          let errorMsg = 'Unknown error';
          if (error.status === 409) {
            errorMsg = 'E-Mail already in list.';
          } else if (error.status === 502) {
            errorMsg = 'Could not send e-mail to this address. Try again!';
          }
          this.snackBar.open(errorMsg, 'Close', {
            duration: 2000,
          });
        }
      );
  }
}
