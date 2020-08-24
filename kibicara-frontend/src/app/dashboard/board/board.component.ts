import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { HoodsService, BodyHood } from 'src/app/core/api';
import { first } from 'rxjs/operators';
import { Observable } from 'rxjs';

@Component({
  selector: 'app-board',
  templateUrl: './board.component.html',
  styleUrls: ['./board.component.scss'],
})
export class BoardComponent implements OnInit {
  hoodId: number;
  hood$: Observable<any>;

  constructor(
    private route: ActivatedRoute,
    private hoodService: HoodsService
  ) {}

  ngOnInit(): void {
    this.hoodId = this.route.snapshot.params['id'];
    this.hood$ = this.hoodService.getHood(this.hoodId);
  }
}
