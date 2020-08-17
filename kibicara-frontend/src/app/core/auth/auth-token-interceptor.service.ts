import { Injectable } from '@angular/core';
import { HttpRequest, HttpHandler, HttpEvent } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class AuthTokenInterceptorService {
  constructor() {}

  intercept(
    req: HttpRequest<any>,
    next: HttpHandler
  ): Observable<HttpEvent<any>> {
    // const token = this.loginService.token;

    // if (token) {
    //   req = req.clone({
    //     setHeaders: {
    //       Authorization: 'Bearer ' + this.loginService.token,
    //     },
    //   });
    // }
    return next.handle(req);
  }
}
