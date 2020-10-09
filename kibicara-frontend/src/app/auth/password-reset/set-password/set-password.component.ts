import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { MatSnackBar } from '@angular/material/snack-bar';
import { ActivatedRoute, Router } from '@angular/router';
import { first } from 'rxjs/operators';
import { AdminService } from 'src/app/core/api/api/admin.service';
import { LoginService } from 'src/app/core/auth/login.service';

@Component({
  selector: 'app-set-password',
  templateUrl: './set-password.component.html',
  styleUrls: ['./set-password.component.scss'],
})
export class SetPasswordComponent implements OnInit {
  resetForm: FormGroup;
  returnUrl: string;
  loading = false;
  submitted = false;
  hide = true;
  token;

  constructor(
    private adminService: AdminService,
    private loginService: LoginService,
    private router: Router,
    private route: ActivatedRoute,
    private formBuilder: FormBuilder,
    private snackBar: MatSnackBar
  ) {
    this.token = this.route.snapshot.queryParams.token;
    if (this.loginService.currentHoodAdminValue) {
      this.router.navigate(['/dashboard']);
    } else if (!this.token) {
      this.router.navigate(['/404']);
    }
  }

  ngOnInit(): void {
    this.resetForm = this.formBuilder.group({
      password: ['', [Validators.required, Validators.minLength(8)]],
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
      .confirmReset(this.token, {
        password: this.resetForm.controls.password.value,
      })
      .pipe(first())
      .subscribe(
        (data) => {
          this.router.navigate([this.returnUrl]);
          this.snackBar.open('Password reset successful!', 'Close', {
            duration: 2000,
          });
        },
        (error) => {
          this.snackBar.open(
            'Error resetting password! Try ordering another password reset email!',
            'Close',
            {
              duration: 2000,
            }
          );
          this.loading = false;
        }
      );
  }
}
