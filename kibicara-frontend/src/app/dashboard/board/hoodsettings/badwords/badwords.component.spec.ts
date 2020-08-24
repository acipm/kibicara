import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { BadwordsComponent } from './badwords.component';

describe('BadwordsComponent', () => {
  let component: BadwordsComponent;
  let fixture: ComponentFixture<BadwordsComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [BadwordsComponent],
    }).compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(BadwordsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
