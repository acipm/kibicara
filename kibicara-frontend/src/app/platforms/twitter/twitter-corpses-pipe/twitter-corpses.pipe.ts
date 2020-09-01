import { Pipe, PipeTransform } from '@angular/core';

@Pipe({
  name: 'twitterCorpses',
})
export class TwitterCorpsesPipe implements PipeTransform {
  transform(twitters) {
    return twitters.filter((x) => x.verified === 1);
  }
}
