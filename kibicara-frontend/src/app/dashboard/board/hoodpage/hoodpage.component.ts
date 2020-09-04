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

  markdown = `# TODO Hoodpage`;

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
