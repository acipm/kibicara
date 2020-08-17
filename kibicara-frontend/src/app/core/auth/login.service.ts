import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { AdminService } from '../api';

@Injectable({
  providedIn: 'root',
})
export class LoginService {
  private currentHoodAdminSubject: BehaviorSubject<any>;
  public currentHoodAdmin: Observable<any>;

  constructor(private readonly adminService: AdminService) {
    this.currentHoodAdminSubject = new BehaviorSubject<any>(
      JSON.parse(localStorage.getItem('currentHoodAdmin'))
    );
    this.currentHoodAdmin = this.currentHoodAdminSubject.asObservable();
  }

  public get currentHoodAdminValue() {
    return this.currentHoodAdminSubject.value;
  }

  login(email, password) {
    return this.adminService.login(email, password).pipe(
      map((response) => {
        localStorage.setItem('currentHoodAdmin', JSON.stringify(response));
        this.currentHoodAdminSubject.next(response);
        return response;
      })
    );
  }

  logout() {
    localStorage.removeItem('currentHoodAdmin');
    this.currentHoodAdminSubject.next(null);
  }
}
