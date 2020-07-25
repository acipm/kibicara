import { NgModule } from '@angular/core';
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatMenuModule } from '@angular/material/menu';

@NgModule({
  declarations: [],
  imports: [MatButtonModule, MatIconModule, MatMenuModule, MatToolbarModule],
  exports: [MatButtonModule, MatIconModule, MatMenuModule, MatToolbarModule],
})
export class MaterialModule {}
