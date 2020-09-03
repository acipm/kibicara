import { Component, OnInit, Input } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { PlatformsInfoDialogComponent } from './platforms-info-dialog/platforms-info-dialog.component';

@Component({
  selector: 'app-platforms-info-page',
  templateUrl: './platforms-info-page.component.html',
  styleUrls: ['./platforms-info-page.component.scss'],
})
export class PlatformsInfoPageComponent implements OnInit {
  @Input() hoodId;

  constructor(private dialog: MatDialog) {}

  ngOnInit(): void {}

  onInfoClick() {
    this.dialog.open(PlatformsInfoDialogComponent);
  }
}
