import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { PublicPagesComponent } from './public-pages.component';

describe('PublicPagesComponent', () => {
  let component: PublicPagesComponent;
  let fixture: ComponentFixture<PublicPagesComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ PublicPagesComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(PublicPagesComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
