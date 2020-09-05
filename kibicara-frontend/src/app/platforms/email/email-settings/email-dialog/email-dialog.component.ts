import { Component, OnInit, Input, Inject } from '@angular/core';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { Validators, FormBuilder } from '@angular/forms';
import { EmailService } from 'src/app/core/api';
import { first } from 'rxjs/operators';
import { MatSnackBar } from '@angular/material/snack-bar';

@Component({
  selector: 'app-email-dialog',
  templateUrl: './email-dialog.component.html',
  styleUrls: ['./email-dialog.component.scss'],
})
export class EmailDialogComponent implements OnInit {
  form;

  constructor(
    public dialogRef: MatDialogRef<EmailDialogComponent>,
    private formBuilder: FormBuilder,
    private emailService: EmailService,
    private snackBar: MatSnackBar,
    @Inject(MAT_DIALOG_DATA) public data
  ) {}

  ngOnInit(): void {
    this.form = this.formBuilder.group({
      name: ['', Validators.required],
    });
  }

  onCancel() {
    this.dialogRef.close();
  }

  onSubmit() {
    if (this.form.invalid) {
      return;
    }
    this.emailService
      .createEmail(this.data.hoodId, {
        name: 'kibicara-' + this.form.controls.name.value,
      })
      .pipe(first())
      .subscribe(
        (data) => {
          this.dialogRef.close();
        },
        (error) => {
          this.snackBar.open('Address already taken', 'Close', {
            duration: 2000,
          });
        }
      );
  }
}
