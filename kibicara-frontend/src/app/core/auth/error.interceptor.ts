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
import { MatSnackBar } from '@angular/material/snack-bar';
import { OverlayComponent } from 'src/app/shared/overlay/overlay.component';

@Injectable()
export class ErrorInterceptor implements HttpInterceptor {
  constructor(
    private loginService: LoginService,
    private router: Router,
    private snackBar: MatSnackBar
  ) {}

  intercept(
    request: HttpRequest<unknown>,
    next: HttpHandler
  ): Observable<HttpEvent<any>> {
    return next.handle(request).pipe(
      catchError((err: HttpErrorResponse) => {
        if (err.error instanceof ProgressEvent) {
          // TODO Add spinner/overlay in app to prevent user input
          console.log('Networkerror');
          this.snackBar.openFromComponent(OverlayComponent, {
            verticalPosition: 'top',
          });
          setTimeout(() => {
            window.location.reload();
          }, 20000);
        } else if (err.status === 401) {
          this.loginService.logout();
          location.reload();
        } else if (err.status === 404) {
          this.router.navigate(['/404']);
        }
        const error = err.error.message || err.statusText;
        return throwError(error);
      })
    );
  }
}
