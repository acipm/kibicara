import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { PlatformsInfoPageComponent } from './platforms-info-page.component';

describe('PlatformsInfoPageComponent', () => {
  let component: PlatformsInfoPageComponent;
  let fixture: ComponentFixture<PlatformsInfoPageComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [PlatformsInfoPageComponent],
    }).compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(PlatformsInfoPageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
