import { Component, OnInit, Input } from '@angular/core';
import { Observable } from 'rxjs/internal/Observable';
import { EmailService } from 'src/app/core/api';

@Component({
  selector: 'app-email-settings',
  templateUrl: './email-settings.component.html',
  styleUrls: ['./email-settings.component.scss'],
})
export class EmailSettingsComponent implements OnInit {
  @Input() hoodId;
  emails$: Observable<Array<any>>;

  constructor(private emailService: EmailService) {}

  ngOnInit(): void {
    this.emails$ = this.emailService.getEmails(this.hoodId);
  }
}
