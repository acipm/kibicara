import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { TelegramDialogComponent } from './telegram-dialog.component';

describe('TelegramDialogComponent', () => {
  let component: TelegramDialogComponent;
  let fixture: ComponentFixture<TelegramDialogComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [TelegramDialogComponent],
    }).compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(TelegramDialogComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
