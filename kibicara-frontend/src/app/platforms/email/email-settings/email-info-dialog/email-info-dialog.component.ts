import { Component, OnInit } from '@angular/core';
import { environment } from 'src/environments/environment';

@Component({
  selector: 'app-email-info-dialog',
  templateUrl: './email-info-dialog.component.html',
  styleUrls: ['./email-info-dialog.component.scss'],
})
export class EmailInfoDialogComponent implements OnInit {
  domain = environment.EMAIL_DOMAIN;
  constructor() {}

  ngOnInit(): void {}
}
