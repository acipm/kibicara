import { Component, OnInit, Input } from '@angular/core';
import { Observable } from 'rxjs';
import { TwitterService } from 'src/app/core/api';
import { TwitterInfoDialogComponent } from './twitter-info-dialog/twitter-info-dialog.component';
import { MatDialog } from '@angular/material/dialog';
import { MatSnackBar } from '@angular/material/snack-bar';

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
    public dialog: MatDialog,
    private snackBar: MatSnackBar
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

  onChange(twitter) {
    if (twitter.enabled === 0) {
      this.twitterService.startTwitter(twitter.id, this.hoodId).subscribe(
        () => {},
        (error) => {
          this.snackBar.open('Could not start. Check your settings.', 'Close', {
            duration: 2000,
          });
        }
      );
    } else if (twitter.enabled === 1) {
      this.twitterService.stopTwitter(twitter.id, this.hoodId).subscribe(
        () => {},
        (error) => {
          this.snackBar.open('Could not stop. Check your settings.', 'Close', {
            duration: 2000,
          });
        }
      );
    }
    // TODO yeah i know this is bad, implement disabling/enabling
    setTimeout(() => {
      this.reload();
    }, 100);
  }
}
