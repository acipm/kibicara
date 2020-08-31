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
    this.twitters$ = this.twitterService.getTwitters(this.hoodId);
  }

  onInfoClick() {
    this.dialog.open(TwitterInfoDialogComponent);
  }
}
