import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { HoodsService, BodyHood } from '../../core/api';
import { first } from 'rxjs/operators';

@Component({
  selector: 'app-hoodpage',
  templateUrl: './hoodpage.component.html',
  styleUrls: ['./hoodpage.component.scss'],
})
export class HoodpageComponent implements OnInit {
  hoodId;
  hood: BodyHood;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private readonly hoodsService: HoodsService
  ) {}

  ngOnInit(): void {
    this.hoodId = this.route.snapshot.params.id;
    if (this.hoodId) {
      this.hoodsService
        .getHood(this.hoodId)
        .pipe(first())
        .subscribe((data) => {
          this.hood = data;
        });
    }
  }
}
