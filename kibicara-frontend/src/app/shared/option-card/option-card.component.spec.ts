import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { OptionCardComponent } from './option-card.component';

describe('OptionCardComponent', () => {
  let component: OptionCardComponent;
  let fixture: ComponentFixture<OptionCardComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [OptionCardComponent],
    }).compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(OptionCardComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
