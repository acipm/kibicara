import { Component, OnInit, Input } from '@angular/core';
import { TriggersService, BodyTrigger } from 'src/app/core/api';
import { Observable } from 'rxjs';

@Component({
  selector: 'app-trigger',
  templateUrl: './trigger.component.html',
  styleUrls: ['./trigger.component.scss'],
})
export class TriggerComponent implements OnInit {
  @Input() hoodId: number;
  triggers$: Observable<Array<any>>;

  constructor(private triggersService: TriggersService) {}

  ngOnInit(): void {
    this.triggers$ = this.triggersService.getTriggers(this.hoodId);
  }
}
