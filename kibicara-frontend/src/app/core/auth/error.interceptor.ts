import { Injectable } from '@angular/core';
import {
  HttpRequest,
  HttpHandler,
  HttpEvent,
  HttpInterceptor,
  HttpErrorResponse,
} from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { LoginService } from './login.service';
import { catchError } from 'rxjs/operators';
import { Router } from '@angular/router';

@Injectable()
export class ErrorInterceptor implements HttpInterceptor {
  constructor(private loginService: LoginService, private router: Router) {}

  intercept(
    request: HttpRequest<unknown>,
    next: HttpHandler
  ): Observable<HttpEvent<any>> {
    return next.handle(request).pipe(
      catchError((err: HttpErrorResponse) => {
        if (err.error instanceof ProgressEvent) {
          // TODO Add spinner/overlay in app to prevent user input
          console.log('Networkerror');
        } else if (err.status === 401) {
          this.loginService.logout();
          location.reload(true);
        } else if (err.status === 404) {
          this.router.navigate(['/404']);
        }
        const error = err.error.message || err.statusText;
        return throwError(error);
      })
    );
  }
}
