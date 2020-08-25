import { NgModule } from '@angular/core';
import { ToolbarComponent } from './toolbar/toolbar.component';
import { MaterialModule } from './material/material.module';
import { NotFoundComponent } from './not-found/not-found.component';
import { ReactiveFormsModule, FormsModule } from '@angular/forms';
import { MarkdownModule } from 'ngx-markdown';
import { HttpClient } from '@angular/common/http';

@NgModule({
  declarations: [ToolbarComponent, NotFoundComponent],
  imports: [MaterialModule, ReactiveFormsModule, FormsModule],
  exports: [
    ToolbarComponent,
    NotFoundComponent,
    MaterialModule,
    ReactiveFormsModule,
    FormsModule,
  ],
})
export class SharedModule {}
