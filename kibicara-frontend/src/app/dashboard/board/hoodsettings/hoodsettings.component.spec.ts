import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { HoodsettingsComponent } from './hoodsettings.component';

describe('HoodsettingsComponent', () => {
  let component: HoodsettingsComponent;
  let fixture: ComponentFixture<HoodsettingsComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [HoodsettingsComponent],
    }).compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(HoodsettingsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
