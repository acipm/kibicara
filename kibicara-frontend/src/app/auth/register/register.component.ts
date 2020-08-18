import { Component, OnInit } from '@angular/core';
import { AdminService } from '../../core/api';
import { Validators, FormBuilder, FormGroup } from '@angular/forms';
import { first } from 'rxjs/operators';
import { Router, ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.scss'],
})
export class RegisterComponent implements OnInit {
  registerForm: FormGroup;
  loading = false;
  submitted = false;
  error: string;
  info: string;

  constructor(
    private readonly adminService: AdminService,
    private formBuilder: FormBuilder,
    private route: ActivatedRoute
  ) {}

  ngOnInit(): void {
    this.registerForm = this.formBuilder.group({
      email: ['', Validators.required],
      password: ['', [Validators.required, Validators.minLength(6)]],
    });

    if (this.route.snapshot.queryParams['error']) {
      this.error = 'Invalid confirmation link. Try registering again';
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
          this.info =
            'Registration E-Mail has been sent. Please check your inbox.';
          this.loading = false;
        },
        (error) => {
          this.error = 'Registration failed! E-Mail exists or is not valid.';
          this.loading = false;
        }
      );
  }
}
