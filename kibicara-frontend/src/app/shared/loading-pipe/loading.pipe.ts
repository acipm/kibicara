import { Pipe, PipeTransform } from '@angular/core';
import { map, startWith, catchError } from 'rxjs/operators';
import { of, isObservable } from 'rxjs';

@Pipe({
  name: 'loading',
})
export class LoadingPipe implements PipeTransform {
  transform(val) {
    return isObservable(val)
      ? val.pipe(
          map((value: any) => ({ loading: false, value })),
          startWith({ loading: true }),
          catchError((error) => of({ loading: false, error }))
        )
      : val;
  }
}
