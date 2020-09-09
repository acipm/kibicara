import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { HoodspageComponent } from './hoodspage.component';

describe('HoodspageComponent', () => {
  let component: HoodspageComponent;
  let fixture: ComponentFixture<HoodspageComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ HoodspageComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(HoodspageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
