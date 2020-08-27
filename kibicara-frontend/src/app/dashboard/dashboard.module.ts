import { NgModule } from '@angular/core';
import { HoodsComponent } from './hoods/hoods.component';
import { DashboardComponent } from './dashboard.component';
import { DashboardRoutingModule } from './dashboard-routing.module';
import { HoodsettingsComponent } from './board/hoodsettings/hoodsettings.component';
import { PlatformsComponent } from './board/platforms/platforms.component';
import { HoodpageComponent } from './board/hoodpage/hoodpage.component';
import { BoardComponent } from './board/board.component';
import { MaterialModule } from '../shared/material/material.module';
import { TriggerComponent } from './board/hoodsettings/trigger/trigger.component';
import { BadwordsComponent } from './board/hoodsettings/badwords/badwords.component';
import { SharedModule } from '../shared/shared.module';
import { CommonModule } from '@angular/common';
import { MarkdownModule } from 'ngx-markdown';
import { HttpClient } from '@angular/common/http';
import { NewHoodDialogComponent } from './hoods/new-hood-dialog/new-hood-dialog.component';

@NgModule({
  declarations: [
    HoodsComponent,
    DashboardComponent,
    HoodsettingsComponent,
    PlatformsComponent,
    HoodpageComponent,
    BoardComponent,
    TriggerComponent,
    BadwordsComponent,
    NewHoodDialogComponent,
  ],
  imports: [
    DashboardRoutingModule,
    MaterialModule,
    SharedModule,
    CommonModule,
    MarkdownModule.forRoot({ loader: HttpClient }),
  ],
})
export class DashboardModule {}
