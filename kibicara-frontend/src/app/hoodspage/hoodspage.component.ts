import { Component, OnInit } from '@angular/core';
import { HoodsService } from '../core/api/api/hoods.service';

@Component({
  selector: 'app-hoodspage',
  templateUrl: './hoodspage.component.html',
  styleUrls: ['./hoodspage.component.scss'],
})
export class HoodspageComponent implements OnInit {
  hoods$;
  searchText: string;
  title = 'Discover hoods';

  constructor(private readonly hoodsService: HoodsService) {}

  ngOnInit(): void {
    this.hoods$ = this.hoodsService.getHoods();
  }
}
