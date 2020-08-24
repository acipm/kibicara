import { NgModule } from '@angular/core';
import { ToolbarComponent } from './toolbar/toolbar.component';
import { MaterialModule } from './material/material.module';
import { NotFoundComponent } from './not-found/not-found.component';
import { ReactiveFormsModule } from '@angular/forms';

@NgModule({
  declarations: [ToolbarComponent, NotFoundComponent],
  imports: [MaterialModule, ReactiveFormsModule],
  exports: [
    ToolbarComponent,
    NotFoundComponent,
    MaterialModule,
    ReactiveFormsModule,
  ],
})
export class SharedModule {}
