import { Component, OnInit, Input } from '@angular/core';

@Component({
  selector: 'app-platforms',
  templateUrl: './platforms.component.html',
  styleUrls: ['./platforms.component.scss'],
})
export class PlatformsComponent implements OnInit {
  @Input() hoodId;

  constructor() {}

  ngOnInit(): void {}
}
