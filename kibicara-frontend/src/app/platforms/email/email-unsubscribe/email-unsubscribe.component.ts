import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { EmailService } from 'src/app/core/api';
import { MatSnackBar } from '@angular/material/snack-bar';

@Component({
  selector: 'app-email-unsubscribe',
  templateUrl: './email-unsubscribe.component.html',
  styleUrls: ['./email-unsubscribe.component.scss'],
})
export class EmailUnsubscribeComponent implements OnInit {
  status = '';

  constructor(
    private route: ActivatedRoute,
    private emailService: EmailService,
    private router: Router,
    private snackBar: MatSnackBar
  ) {}

  ngOnInit(): void {
    if (
      this.route.snapshot.params.id &&
      this.route.snapshot.queryParams.token
    ) {
      console.log(this.route.snapshot.params.id);
      this.emailService
        .unsubscribe(
          this.route.snapshot.queryParams.token,
          this.route.snapshot.params.id
        )
        .subscribe(() => {
          this.status = 'You were successfully unsubscribed.';
        });
    } else {
      this.router.navigate(['/404']);
    }
  }
}
