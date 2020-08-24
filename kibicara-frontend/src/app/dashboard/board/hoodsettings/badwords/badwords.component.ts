import { Component, OnInit, Input } from '@angular/core';
import { BadwordsService, BodyBadWord } from 'src/app/core/api';
import { Observable } from 'rxjs';

@Component({
  selector: 'app-badwords',
  templateUrl: './badwords.component.html',
  styleUrls: ['./badwords.component.scss'],
})
export class BadwordsComponent implements OnInit {
  @Input() hoodId;
  badwords$: Observable<BodyBadWord>;

  constructor(private badwordService: BadwordsService) {}

  ngOnInit(): void {
    //this.badwords$ = this.badwordService.getBadwords(this.hoodId);
  }
}
