import { Component, OnInit, Input } from '@angular/core';

@Component({
  selector: 'app-hoodsettings',
  templateUrl: './hoodsettings.component.html',
  styleUrls: ['./hoodsettings.component.scss'],
})
export class HoodsettingsComponent implements OnInit {
  @Input() hoodId;

  constructor() {}

  ngOnInit(): void {}
}
