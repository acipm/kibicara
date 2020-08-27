import { Component, OnInit } from '@angular/core';
import { AdminService } from '../../core/api';
import { Validators, FormBuilder, FormGroup } from '@angular/forms';
import { first } from 'rxjs/operators';
import { Router, ActivatedRoute } from '@angular/router';
import { LoginService } from 'src/app/core/auth/login.service';
import { MatSnackBar } from '@angular/material/snack-bar';

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.scss'],
})
export class RegisterComponent implements OnInit {
  registerForm: FormGroup;
  loading = false;
  submitted = false;

  constructor(
    private readonly adminService: AdminService,
    private formBuilder: FormBuilder,
    private route: ActivatedRoute,
    private loginService: LoginService,
    private router: Router,
    private snackBar: MatSnackBar
  ) {
    if (this.loginService.currentHoodAdminValue) {
      this.router.navigate(['/dashboard']);
    }
  }

  ngOnInit(): void {
    this.registerForm = this.formBuilder.group({
      email: ['', Validators.required],
      password: ['', [Validators.required, Validators.minLength(8)]],
    });

    if (this.route.snapshot.queryParams['error']) {
      this.snackBar.open(
        'Invalid confirmation link. Try registering again',
        'Close',
        {
          duration: 2000,
        }
      );
    }
  }

  onSubmit() {
    this.submitted = true;
    if (this.registerForm.invalid) {
      return;
    }
    this.loading = true;
    this.adminService
      .register(this.registerForm.value)
      .pipe(first())
      .subscribe(
        (data) => {
          this.snackBar.open(
            'Registration E-Mail has been sent. Please check your inbox.',
            'Close',
            {
              duration: 2000,
            }
          );
          this.loading = false;
        },
        (error) => {
          this.snackBar.open(
            'Registration failed! E-Mail exists or is not valid.',
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
