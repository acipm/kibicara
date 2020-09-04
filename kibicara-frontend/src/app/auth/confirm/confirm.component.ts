import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { AdminService } from '../../core/api';
import { first } from 'rxjs/operators';

@Component({
  selector: 'app-confirm',
  templateUrl: './confirm.component.html',
  styleUrls: ['./confirm.component.scss'],
})
export class ConfirmComponent implements OnInit {
  constructor(
    private route: ActivatedRoute,
    private adminService: AdminService,
    private router: Router
  ) {}

  ngOnInit(): void {
    const token = this.route.snapshot.queryParams.token;
    if (token) {
      this.adminService
        .confirm(token)
        .pipe(first())
        .subscribe(
          (data) => {
            this.router.navigate(['/login'], {
              queryParams: { registered: true },
            });
          },
          (error) => {
            this.router.navigate(['/register'], {
              queryParams: { error: true },
            });
          }
        );
    } else {
      this.router.navigate(['/register']);
    }
  }
}
