import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { MatDialog } from '@angular/material/dialog';
import { Router } from '@angular/router';
import { AdminService } from 'src/app/core/api/api/admin.service';
import { YesNoDialogComponent } from 'src/app/shared/yes-no-dialog/yes-no-dialog.component';

@Component({
  selector: 'app-account-settings',
  templateUrl: './account-settings.component.html',
  styleUrls: ['./account-settings.component.scss'],
})
export class AccountSettingsComponent implements OnInit {
  title = 'Account Settings';
  form: FormGroup;

  constructor(
    private dialog: MatDialog,
    private adminService: AdminService,
    private router: Router,
    private formBuilder: FormBuilder
  ) {}

  ngOnInit(): void {
    this.form = this.formBuilder.group({
      email: ['', Validators.required],
      password: ['', [Validators.required, Validators.minLength(8)]],
    });
  }

  onUpdate() {}

  onDelete() {
    const dialogRef = this.dialog.open(YesNoDialogComponent, {
      data: {
        title: 'Warning',
        content: 'This will also delete all of your hoods and bots.',
      },
    });

    dialogRef.afterClosed().subscribe((response) => {
      if (response) {
        this.adminService.deleteAdmin().subscribe(() => {
          this.router.navigate(['/dashboard']);
        });
      }
    });
  }
}
