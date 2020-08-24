import { Component, OnInit, Input } from '@angular/core';
import { TriggersService, BodyTrigger } from 'src/app/core/api';
import { Observable } from 'rxjs';
import { ResourceLoader } from '@angular/compiler';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { first } from 'rxjs/operators';
import { invalid } from '@angular/compiler/src/render3/view/util';

@Component({
  selector: 'app-trigger',
  templateUrl: './trigger.component.html',
  styleUrls: ['./trigger.component.scss'],
})
export class TriggerComponent implements OnInit {
  @Input() hoodId: number;
  triggers$: Observable<Array<any>>;
  regexForm: FormGroup;

  constructor(
    private triggersService: TriggersService,
    private formBuilder: FormBuilder
  ) {}

  ngOnInit(): void {
    this.reload();
    this.regexForm = this.formBuilder.group({
      regex: ['', Validators.required],
    });
  }

  private reload() {
    this.triggers$ = this.triggersService.getTriggers(this.hoodId);
  }

  onEdit(triggerId) {}

  onDelete(triggerId) {
    this.triggersService.deleteTrigger(triggerId, this.hoodId).subscribe(() => {
      this.reload();
    });
  }

  onSubmit() {
    if (this.regexForm.invalid) {
      return;
    }

    this.triggersService
      .createTrigger(this.hoodId, {
        pattern: this.regexForm.controls.regex.value,
      })
      .pipe(first())
      .subscribe(
        (data) => {
          this.regexForm.reset();
          this.reload();
        },
        (error) => {
          console.log(error);
          this.regexForm.controls['regex'].setErrors({ incorrect: true });
        }
      );
  }
}
