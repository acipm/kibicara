import { Component, OnInit } from '@angular/core';
import { AdminService, BodyHood } from 'src/app/core/api';
import { map } from 'rxjs/operators';
import { Observer } from 'rxjs';
import { MatDialog } from '@angular/material/dialog';
import { NewHoodDialogComponent } from './new-hood-dialog/new-hood-dialog.component';
import { Router } from '@angular/router';

@Component({
  selector: 'app-hoods',
  templateUrl: './hoods.component.html',
  styleUrls: ['./hoods.component.scss'],
})
export class HoodsComponent implements OnInit {
  hoods$;

  constructor(
    private readonly adminService: AdminService,
    public dialog: MatDialog,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.hoods$ = this.adminService.getHoodsAdmin().pipe(
      map((hoods) => {
        const result = hoods.map((hood) => {
          return hood.hood;
        });
        return result;
      })
    );
  }

  openNewHoodDialog() {
    const dialogRef = this.dialog.open(NewHoodDialogComponent);

    dialogRef.afterClosed().subscribe((hood) => {
      if (hood && hood.id) {
        this.router.navigate(['/dashboard/hoods', hood.id]);
      }
    });
  }
}
