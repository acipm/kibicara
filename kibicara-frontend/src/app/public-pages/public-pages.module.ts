import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HomepageComponent } from './homepage/homepage.component';
import { HoodspageComponent } from './hoodspage/hoodspage.component';
import { HoodpageComponent } from './hoodpage/hoodpage.component';
import { OrganizerspageComponent } from './organizerspage/organizerspage.component';
import { FaqComponent } from './homepage/faq/faq.component';
import { SharedModule } from '../shared/shared.module';
import { PlatformsModule } from '../platforms/platforms.module';
import { MarkdownModule } from 'ngx-markdown';
import { HttpClient } from '@angular/common/http';
import { PublicPagesComponent } from './public-pages.component';
import { PublicPagesRoutingModule } from './public-pages-routing.module';

@NgModule({
  declarations: [
    HomepageComponent,
    HoodspageComponent,
    HoodpageComponent,
    OrganizerspageComponent,
    FaqComponent,
    PublicPagesComponent,
  ],
  imports: [
    SharedModule,
    PlatformsModule,
    MarkdownModule.forRoot({ loader: HttpClient }),
    PublicPagesRoutingModule,
  ],
  exports: [
    HomepageComponent,
    HoodspageComponent,
    HoodpageComponent,
    OrganizerspageComponent,
  ],
})
export class PublicPagesModule {}
