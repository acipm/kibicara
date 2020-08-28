import { Component, OnInit, Input } from '@angular/core';
import { TelegramService } from 'src/app/core/api';
import { Observer, Observable } from 'rxjs';

@Component({
  selector: 'app-telegram-settings',
  templateUrl: './telegram-settings.component.html',
  styleUrls: ['./telegram-settings.component.scss'],
})
export class TelegramSettingsComponent implements OnInit {
  @Input() hoodId;
  telegrams$: Observable<Array<any>>;

  constructor(private telegramService: TelegramService) {}

  ngOnInit(): void {
    this.telegrams$ = this.telegramService.getTelegrams(this.hoodId);
  }
}
