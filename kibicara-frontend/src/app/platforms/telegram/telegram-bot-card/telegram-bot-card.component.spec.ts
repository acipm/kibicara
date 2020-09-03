import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { TelegramBotCardComponent } from './telegram-bot-card.component';

describe('TelegramBotCardComponent', () => {
  let component: TelegramBotCardComponent;
  let fixture: ComponentFixture<TelegramBotCardComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [TelegramBotCardComponent],
    }).compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(TelegramBotCardComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
