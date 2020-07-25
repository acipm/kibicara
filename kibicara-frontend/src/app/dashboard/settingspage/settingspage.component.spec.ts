import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { SettingspageComponent } from './settingspage.component';

describe('SettingspageComponent', () => {
  let component: SettingspageComponent;
  let fixture: ComponentFixture<SettingspageComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ SettingspageComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(SettingspageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
