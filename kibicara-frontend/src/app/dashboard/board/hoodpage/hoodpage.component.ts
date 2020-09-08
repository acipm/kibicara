import { Component, OnInit, Input } from '@angular/core';
import { HoodsService, BodyHood } from 'src/app/core/api';
import { first } from 'rxjs/operators';

@Component({
  selector: 'app-hoodpage',
  templateUrl: './hoodpage.component.html',
  styleUrls: ['./hoodpage.component.scss'],
})
export class HoodpageComponent implements OnInit {
  @Input() hoodId: number;
  saved = false;
  submit = false;
  hood: BodyHood;

  constructor(private hoodsService: HoodsService) {}

  markdown = `## Welcome to the hood!
  
  We are a community in xyz-city that supports each other. 
  Here you can find all platforms where you can communicate
  to members of communities and announce neighborhood festivals,
  ask your neighbors for help or just make contact.
  
  You only need one of the plaforms below. 
  Subscribe to this hood as described. If you want to broadcast a message just
  tweet/direct message/mail to the subscribed platform as you know it and the
  bots will distribute your message to all subscribers on other platforms.
  `;

  ngOnInit(): void {
    this.hoodsService.getHood(this.hoodId).subscribe((hood) => {
      if (hood) {
        this.hood = hood;
        if (hood.landingpage && hood.landingpage !== '') {
          this.markdown = hood.landingpage;
        }
      }
    });
  }

  onSubmit() {
    this.submit = true;
    this.hood.landingpage = this.markdown;
    this.hoodsService
      .updateHood(this.hoodId, this.hood)
      .pipe(first())
      .subscribe(
        (data) => {
          this.saved = true;
        },
        (error) => {
          this.saved = false;
        }
      );
  }

  onChange() {
    this.saved = false;
    this.submit = false;
  }
}
