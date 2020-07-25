import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { HoodsComponent } from './hoods.component';

describe('HoodsComponent', () => {
  let component: HoodsComponent;
  let fixture: ComponentFixture<HoodsComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ HoodsComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(HoodsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
