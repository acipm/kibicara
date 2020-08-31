import { Component, OnInit, Input } from '@angular/core';
import { Observable } from 'rxjs';
import { TwitterService } from 'src/app/core/api';
import { TwitterInfoDialogComponent } from '../twitter-info-dialog/twitter-info-dialog.component';
import { MatDialog } from '@angular/material/dialog';

@Component({
  selector: 'app-twitter-settings',
  templateUrl: './twitter-settings.component.html',
  styleUrls: ['./twitter-settings.component.scss'],
})
export class TwitterSettingsComponent implements OnInit {
  @Input() hoodId;
  twitters$: Observable<Array<any>>;

  constructor(
    private twitterService: TwitterService,
    public dialog: MatDialog
  ) {}

  ngOnInit(): void {
    this.reload();
  }

  private reload() {
    this.twitters$ = this.twitterService.getTwitters(this.hoodId);
  }

  onInfoClick() {
    this.dialog.open(TwitterInfoDialogComponent);
  }

  onDelete(twitterId) {
    this.twitterService.deleteTwitter(twitterId, this.hoodId).subscribe(() => {
      this.reload();
    });
  }

  onCreate() {
    this.twitterService.createTwitter(this.hoodId).subscribe((twitter) => {
      if (twitter && twitter.access_token) {
        const redirectUrl =
          'https://api.twitter.com/oauth/authorize?oauth_token=' +
          twitter.access_token;
        window.location.href = redirectUrl;
      }
    });
  }
}
