import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { TelegramInfoDialogComponent } from './telegram-info-dialog.component';

describe('TelegramInfoDialogComponent', () => {
  let component: TelegramInfoDialogComponent;
  let fixture: ComponentFixture<TelegramInfoDialogComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [TelegramInfoDialogComponent],
    }).compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(TelegramInfoDialogComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
