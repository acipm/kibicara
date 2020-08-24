import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { HoodpageComponent } from './hoodpage.component';

describe('HoodpageComponent', () => {
  let component: HoodpageComponent;
  let fixture: ComponentFixture<HoodpageComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [HoodpageComponent],
    }).compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(HoodpageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
