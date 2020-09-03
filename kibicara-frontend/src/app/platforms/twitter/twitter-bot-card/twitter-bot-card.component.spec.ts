import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { TwitterBotCardComponent } from './twitter-bot-card.component';

describe('TwitterBotCardComponent', () => {
  let component: TwitterBotCardComponent;
  let fixture: ComponentFixture<TwitterBotCardComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [TwitterBotCardComponent],
    }).compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(TwitterBotCardComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
