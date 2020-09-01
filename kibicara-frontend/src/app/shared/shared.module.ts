import { NgModule } from '@angular/core';
import { ToolbarComponent } from './toolbar/toolbar.component';
import { MaterialModule } from './material/material.module';
import { NotFoundComponent } from './not-found/not-found.component';
import { ReactiveFormsModule, FormsModule } from '@angular/forms';
import { RouterModule } from '@angular/router';
import { CommonModule } from '@angular/common';
import { Ng2SearchPipeModule } from 'ng2-search-filter';
import { YesNoDialogComponent } from './yes-no-dialog/yes-no-dialog.component';

@NgModule({
  declarations: [ToolbarComponent, NotFoundComponent, YesNoDialogComponent],
  imports: [
    MaterialModule,
    ReactiveFormsModule,
    FormsModule,
    RouterModule,
    CommonModule,
    Ng2SearchPipeModule,
  ],
  exports: [
    ToolbarComponent,
    NotFoundComponent,
    MaterialModule,
    ReactiveFormsModule,
    FormsModule,
    CommonModule,
    Ng2SearchPipeModule,
  ],
})
export class SharedModule {}
