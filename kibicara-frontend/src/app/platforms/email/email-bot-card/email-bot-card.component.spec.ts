import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { EmailBotCardComponent } from './email-bot-card.component';

describe('EmailBotCardComponent', () => {
  let component: EmailBotCardComponent;
  let fixture: ComponentFixture<EmailBotCardComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [EmailBotCardComponent],
    }).compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(EmailBotCardComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
