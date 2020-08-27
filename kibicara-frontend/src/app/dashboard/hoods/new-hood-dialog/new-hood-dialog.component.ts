import { Component, OnInit, Inject } from '@angular/core';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { HoodsService } from 'src/app/core/api';
import { first } from 'rxjs/operators';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';

@Component({
  selector: 'app-new-hood-dialog',
  templateUrl: './new-hood-dialog.component.html',
  styleUrls: ['./new-hood-dialog.component.scss'],
})
export class NewHoodDialogComponent implements OnInit {
  hoodForm: FormGroup;

  constructor(
    public dialogRef: MatDialogRef<NewHoodDialogComponent>,
    private hoodsService: HoodsService,
    private formBuilder: FormBuilder
  ) {}

  ngOnInit(): void {
    this.hoodForm = this.formBuilder.group({
      hoodName: ['', Validators.required],
    });
  }

  onCancel() {
    this.dialogRef.close();
  }

  onSubmit() {
    if (this.hoodForm.invalid) {
      return;
    }

    this.hoodsService
      .createHood({
        name: this.hoodForm.controls.hoodName.value,
        landingpage: '',
      })
      .pipe(first())
      .subscribe(
        (data) => {
          this.dialogRef.close(data);
        },
        (error) => {
          this.hoodForm.controls['hoodName'].setErrors({ incorrect: true });
        }
      );
  }
}
