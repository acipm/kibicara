import { Component, OnInit, Input } from '@angular/core';
import { BadwordsService, BodyBadWord } from 'src/app/core/api';
import { Observable } from 'rxjs';
import { FormGroup, Validators, FormBuilder } from '@angular/forms';
import { first } from 'rxjs/operators';

@Component({
  selector: 'app-badwords',
  templateUrl: './badwords.component.html',
  styleUrls: ['./badwords.component.scss'],
})
export class BadwordsComponent implements OnInit {
  @Input() hoodId;
  badwords$: Observable<Array<any>>;
  regexForm: FormGroup;

  constructor(
    private badwordService: BadwordsService,
    private formBuilder: FormBuilder
  ) {}

  ngOnInit(): void {
    this.reload();
    this.regexForm = this.formBuilder.group({
      regex: ['', Validators.required],
    });
  }

  private reload() {
    this.badwords$ = this.badwordService.getBadwords(this.hoodId);
  }

  onEdit(triggerId) {}

  onDelete(triggerId) {
    this.badwordService.deleteBadword(triggerId, this.hoodId).subscribe(() => {
      this.reload();
    });
  }

  onSubmit() {
    if (this.regexForm.invalid) {
      return;
    }

    this.badwordService
      .createBadword(this.hoodId, {
        pattern: this.regexForm.controls.regex.value,
      })
      .pipe(first())
      .subscribe(
        (data) => {
          this.regexForm.reset();
          this.reload();
        },
        (error) => {
          this.regexForm.controls['regex'].setErrors({ incorrect: true });
        }
      );
  }
}
