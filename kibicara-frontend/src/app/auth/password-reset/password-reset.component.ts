import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { MatSnackBar } from '@angular/material/snack-bar';
import { ActivatedRoute, Router } from '@angular/router';
import { first } from 'rxjs/operators';
import { AdminService } from 'src/app/core/api/api/admin.service';
import { LoginService } from 'src/app/core/auth/login.service';

@Component({
  selector: 'app-password-reset',
  templateUrl: './password-reset.component.html',
  styleUrls: ['./password-reset.component.scss'],
})
export class PasswordResetComponent implements OnInit {
  resetForm: FormGroup;
  returnUrl: string;
  loading = false;
  submitted = false;
  hide = true;

  constructor(
    private adminService: AdminService,
    private loginService: LoginService,
    private router: Router,
    private route: ActivatedRoute,
    private formBuilder: FormBuilder,
    private snackBar: MatSnackBar
  ) {
    if (this.loginService.currentHoodAdminValue) {
      this.router.navigate(['/dashboard']);
    }
  }

  ngOnInit(): void {
    this.resetForm = this.formBuilder.group({
      email: ['', Validators.required],
    });
    this.returnUrl = this.route.snapshot.queryParams.returnUrl || '/dashboard';
  }

  onSubmit() {
    this.submitted = true;
    if (this.resetForm.invalid) {
      return;
    }

    this.loading = true;
    this.adminService
      .reset({ email: this.resetForm.controls.email.value })
      .pipe(first())
      .subscribe(
        (data) => {
          this.router.navigate([this.returnUrl]);
          this.snackBar.open('Reset E-Mail sent!', 'Close', {
            duration: 2000,
          });
        },
        (error) => {
          this.snackBar.open('Error sending E-Mail!', 'Close', {
            duration: 2000,
          });
          this.loading = false;
        }
      );
  }
}
