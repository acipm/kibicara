import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { AdminService, BodyAccessToken } from '../api';

@Injectable({
  providedIn: 'root',
})
export class LoginService {
  private currentHoodAdminSubject: BehaviorSubject<BodyAccessToken>;
  public currentHoodAdmin: Observable<BodyAccessToken>;
  private identifier = 'currentHoodAdmin';

  constructor(private readonly adminService: AdminService) {
    this.currentHoodAdminSubject = new BehaviorSubject<BodyAccessToken>(
      JSON.parse(localStorage.getItem(this.identifier))
    );
    this.currentHoodAdmin = this.currentHoodAdminSubject.asObservable();
  }

  public get currentHoodAdminValue() {
    return this.currentHoodAdminSubject.value;
  }

  login(email, password) {
    return this.adminService.login(email, password).pipe(
      map((response) => {
        localStorage.setItem(this.identifier, JSON.stringify(response));
        this.currentHoodAdminSubject.next(response);
        return response;
      })
    );
  }

  logout() {
    localStorage.removeItem(this.identifier);
    this.currentHoodAdminSubject.next(null);
  }
}
