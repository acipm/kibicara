import { Component, OnInit } from '@angular/core';
import { AdminService } from 'src/app/core/api';
import { map } from 'rxjs/operators';

@Component({
  selector: 'app-hoods',
  templateUrl: './hoods.component.html',
  styleUrls: ['./hoods.component.scss'],
})
export class HoodsComponent implements OnInit {
  hoods$ = this.adminService.getHoodsAdmin().pipe(
    map((hoods) => {
      const result = hoods.map((hood) => {
        return hood.hood;
      });
      return result;
    })
  );

  constructor(private readonly adminService: AdminService) {}

  ngOnInit(): void {}
}
