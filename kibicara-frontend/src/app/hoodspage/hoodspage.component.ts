import { Component, OnInit } from '@angular/core';
import { HoodsService } from '../api/api/hoods.service';

@Component({
  selector: 'app-hoodspage',
  templateUrl: './hoodspage.component.html',
  styleUrls: ['./hoodspage.component.scss'],
})
export class HoodspageComponent implements OnInit {
  hoods$ = this.hoodsService.getHoods();

  constructor(private readonly hoodsService: HoodsService) {}

  ngOnInit(): void {}
}
