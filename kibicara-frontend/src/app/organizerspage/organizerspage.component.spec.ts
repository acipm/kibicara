import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { OrganizerspageComponent } from './organizerspage.component';

describe('OrganizerspageComponent', () => {
  let component: OrganizerspageComponent;
  let fixture: ComponentFixture<OrganizerspageComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ OrganizerspageComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(OrganizerspageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
