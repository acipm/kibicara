import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { EmailService } from 'src/app/core/api';
import { Route } from '@angular/compiler/src/core';
import { MatDialog } from '@angular/material/dialog';
import { MatSnackBar } from '@angular/material/snack-bar';

@Component({
  selector: 'app-email-confirmation',
  templateUrl: './email-confirmation.component.html',
  styleUrls: ['./email-confirmation.component.scss'],
})
export class EmailConfirmationComponent implements OnInit {
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
        .confirmSubscriber(
          this.route.snapshot.queryParams.token,
          this.route.snapshot.params.id
        )
        .subscribe(
          () => {
            this.router.navigate(['/hoods', this.route.snapshot.params.id]);
            this.snackBar.open('Subscription successful!', 'Close', {
              duration: 2000,
            });
          },
          (err) => {
            this.router.navigate(['/hoods', this.route.snapshot.params.id]);
            this.snackBar.open('Error: Email already in list.', 'Close', {
              duration: 2000,
            });
          }
        );
    } else {
      this.router.navigate(['/404']);
    }
  }
}
