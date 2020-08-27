import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { NewHoodDialogComponent } from './new-hood-dialog.component';

describe('NewHoodDialogComponent', () => {
  let component: NewHoodDialogComponent;
  let fixture: ComponentFixture<NewHoodDialogComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [NewHoodDialogComponent],
    }).compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(NewHoodDialogComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
