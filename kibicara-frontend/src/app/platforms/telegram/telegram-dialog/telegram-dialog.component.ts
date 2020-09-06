import { Component, OnInit, Inject } from '@angular/core';
import { Validators, FormBuilder, FormGroup } from '@angular/forms';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { TelegramService, BodyTelegram } from 'src/app/core/api';
import { MatSnackBar } from '@angular/material/snack-bar';
import { first } from 'rxjs/operators';
import { map } from 'rxjs/operators';

@Component({
  selector: 'app-telegram-dialog',
  templateUrl: './telegram-dialog.component.html',
  styleUrls: ['./telegram-dialog.component.scss'],
})
export class TelegramDialogComponent implements OnInit {
  form: FormGroup;

  constructor(
    public dialogRef: MatDialogRef<TelegramDialogComponent>,
    private formBuilder: FormBuilder,
    private telegramService: TelegramService,
    private snackBar: MatSnackBar,
    @Inject(MAT_DIALOG_DATA) public data
  ) {}

  ngOnInit(): void {
    this.form = this.formBuilder.group({
      api_token: ['', Validators.required],
      welcome_message: ['', Validators.required],
    });

    if (this.data.telegramId) {
      this.telegramService
        .getTelegram(this.data.telegramId, this.data.hoodId)
        .subscribe((data) => {
          this.form.controls.api_token.setValue(data.api_token);
          this.form.controls.welcome_message.setValue(data.welcome_message);
        });
    }
  }

  onCancel() {
    this.dialogRef.close();
  }

  success() {
    this.dialogRef.close();
  }

  error() {
    this.snackBar.open('Invalid API Key. Try again!', 'Close', {
      duration: 2000,
    });
  }

  onSubmit() {
    if (this.form.invalid) {
      return;
    }

    const response = {
      api_token: this.form.controls.api_token.value,
      welcome_message: this.form.controls.welcome_message.value,
    };

    if (this.data.telegramId) {
      this.telegramService
        .updateTelegram(this.data.telegramId, this.data.hoodId, response)
        .pipe(first())
        .subscribe(
          () => {
            this.success();
          },
          () => {
            this.error();
          }
        );
    } else {
      this.telegramService
        .createTelegram(this.data.hoodId, response)
        .pipe(first())
        .subscribe(
          () => {
            this.success();
          },
          () => {
            this.error();
          }
        );
    }
  }
}
