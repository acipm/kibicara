import { Component, OnInit, Input } from '@angular/core';
import { HoodsService } from 'src/app/core/api';
import { MatDialog } from '@angular/material/dialog';
import { YesNoDialogComponent } from 'src/app/shared/yes-no-dialog/yes-no-dialog.component';
import { Router } from '@angular/router';
import { FormGroup, FormBuilder, Validators } from '@angular/forms';
import { first } from 'rxjs/operators';
import { MatSnackBar } from '@angular/material/snack-bar';

@Component({
  selector: 'app-settings',
  templateUrl: './settings.component.html',
  styleUrls: ['./settings.component.scss'],
})
export class SettingsComponent implements OnInit {
  @Input() hoodId;
  form: FormGroup;
  hood;

  constructor(
    private hoodsService: HoodsService,
    private dialog: MatDialog,
    private router: Router,
    private formBuilder: FormBuilder,
    private snackBar: MatSnackBar
  ) {}

  ngOnInit(): void {
    this.hoodsService.getHood(this.hoodId).subscribe((hood) => {
      if (hood) {
        this.hood = hood;
      }
    });
    this.form = this.formBuilder.group({
      name: ['', Validators.required],
    });
  }

  onDelete() {
    const dialogRef = this.dialog.open(YesNoDialogComponent, {
      data: {
        title: 'Warning',
        content: 'This will also delete all of your platform connections.',
      },
    });

    dialogRef.afterClosed().subscribe((response) => {
      if (response) {
        this.hoodsService.deleteHood(this.hoodId).subscribe(() => {
          this.router.navigate(['/dashboard']);
        });
      }
    });
  }

  onUpdate() {
    if (this.form.invalid) {
      return;
    }

    this.hood.name = this.form.controls.name.value;
    this.hoodsService
      .updateHood(this.hoodId, this.hood)
      .pipe(first())
      .subscribe(
        (data) => {
          this.form.reset();
          location.reload();
        },
        (error) => {
          this.snackBar.open('Update failed. Try again!', 'Close', {
            duration: 2000,
          });
        }
      );
  }
}
