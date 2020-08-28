import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { EmailInfoDialogComponent } from './email-info-dialog.component';

describe('EmailInfoDialogComponent', () => {
  let component: EmailInfoDialogComponent;
  let fixture: ComponentFixture<EmailInfoDialogComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [EmailInfoDialogComponent],
    }).compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(EmailInfoDialogComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
