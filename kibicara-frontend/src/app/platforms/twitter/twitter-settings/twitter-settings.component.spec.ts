import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { TwitterSettingsComponent } from './twitter-settings.component';

describe('TwitterSettingsComponent', () => {
  let component: TwitterSettingsComponent;
  let fixture: ComponentFixture<TwitterSettingsComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [TwitterSettingsComponent],
    }).compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(TwitterSettingsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
