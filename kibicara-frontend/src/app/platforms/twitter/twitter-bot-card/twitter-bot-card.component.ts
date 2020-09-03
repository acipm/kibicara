import { Component, OnInit, Input } from '@angular/core';
import { TwitterService } from 'src/app/core/api';
import { TwitterBotInfoDialogComponent } from './twitter-bot-info-dialog/twitter-bot-info-dialog.component';
import { MatDialog } from '@angular/material/dialog';

@Component({
  selector: 'app-twitter-bot-card',
  templateUrl: './twitter-bot-card.component.html',
  styleUrls: ['./twitter-bot-card.component.scss'],
})
export class TwitterBotCardComponent implements OnInit {
  @Input() hoodId;
  twitters$;

  constructor(
    private twitterService: TwitterService,
    private dialog: MatDialog
  ) {}

  ngOnInit(): void {
    this.twitters$ = this.twitterService.getTwittersPublic(this.hoodId);
  }

  onInfoClick() {
    this.dialog.open(TwitterBotInfoDialogComponent);
  }
}
