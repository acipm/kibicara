import { Component, OnInit } from '@angular/core';
import { LoginService } from 'src/app/core/auth/login.service';
import { Observer } from 'rxjs';
import { Route } from '@angular/compiler/src/core';
import { Router, NavigationEnd } from '@angular/router';
import { first, map } from 'rxjs/operators';

@Component({
  selector: 'app-toolbar',
  templateUrl: './toolbar.component.html',
  styleUrls: ['./toolbar.component.scss'],
})
export class ToolbarComponent implements OnInit {
  authenticated = false;

  constructor(private loginService: LoginService, private router: Router) {
    this.router.routeReuseStrategy.shouldReuseRoute = () => {
      return false;
    };

    this.router.events.subscribe((event) => {
      if (event instanceof NavigationEnd) {
        this.router.navigated = false;
        if (this.loginService.currentHoodAdminValue) {
          this.authenticated = true;
        } else {
          this.authenticated = false;
        }
      }
    });
  }

  ngOnInit(): void {}

  onLogout() {
    this.loginService.logout();
    this.router.navigate(['/']);
  }
}
