import { NgModule } from '@angular/core';
import { ToolbarComponent } from './toolbar/toolbar.component';
import { MaterialModule } from './material/material.module';
import { NotFoundComponent } from './not-found/not-found.component';

@NgModule({
  declarations: [ToolbarComponent, NotFoundComponent],
  imports: [MaterialModule],
  exports: [ToolbarComponent, NotFoundComponent, MaterialModule],
})
export class SharedModule {}
