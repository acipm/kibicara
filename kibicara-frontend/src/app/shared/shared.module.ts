import { NgModule } from '@angular/core';
import { ToolbarComponent } from './toolbar/toolbar.component';
import { MaterialModule } from './material/material.module';
import { NotFoundComponent } from './not-found/not-found.component';
import { OptionCardComponent } from './option-card/option-card.component';

@NgModule({
  declarations: [ToolbarComponent, NotFoundComponent, OptionCardComponent],
  imports: [MaterialModule],
  exports: [
    ToolbarComponent,
    NotFoundComponent,
    OptionCardComponent,
    MaterialModule,
  ],
})
export class SharedModule {}
