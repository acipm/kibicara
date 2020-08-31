import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { TwitterService } from 'src/app/core/api';

@Component({
  selector: 'app-twitter-callback',
  templateUrl: './twitter-callback.component.html',
  styleUrls: ['./twitter-callback.component.scss'],
})
export class TwitterCallbackComponent implements OnInit {
  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private twitterService: TwitterService
  ) {}

  ngOnInit(): void {
    if (
      this.route.snapshot.queryParams['hood'] &&
      this.route.snapshot.queryParams['oauth_token'] &&
      this.route.snapshot.queryParams['oauth_verifier']
    ) {
      this.twitterService
        .callbackTwitter(
          this.route.snapshot.queryParams['oauth_token'],
          this.route.snapshot.queryParams['oauth_verifier']
        )
        .subscribe(() => {
          this.router.navigate([
            '/dashboard/hoods',
            this.route.snapshot.queryParams['hood'],
          ]);
        });
    } else {
      this.router.navigate(['/404']);
    }
  }
}
