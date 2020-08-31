import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { TwitterInfoDialogComponent } from './twitter-info-dialog.component';

describe('TwitterInfoDialogComponent', () => {
  let component: TwitterInfoDialogComponent;
  let fixture: ComponentFixture<TwitterInfoDialogComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [TwitterInfoDialogComponent],
    }).compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(TwitterInfoDialogComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
