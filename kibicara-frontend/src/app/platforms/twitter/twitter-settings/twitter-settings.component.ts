import { Component, OnInit, Input } from '@angular/core';
import { Observable } from 'rxjs';
import { TwitterService } from 'src/app/core/api';

@Component({
  selector: 'app-twitter-settings',
  templateUrl: './twitter-settings.component.html',
  styleUrls: ['./twitter-settings.component.scss'],
})
export class TwitterSettingsComponent implements OnInit {
  @Input() hoodId;
  twitters$: Observable<Array<any>>;

  constructor(private twitterService: TwitterService) {}

  ngOnInit(): void {
    this.twitters$ = this.twitterService.getTwitters(this.hoodId);
  }
}
