import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { HomepageComponent } from './homepage/homepage.component';
import { PublicPagesComponent } from './public-pages.component';
import { OrganizerspageComponent } from './organizerspage/organizerspage.component';
import { HoodspageComponent } from './hoodspage/hoodspage.component';
import { HoodpageComponent } from './hoodpage/hoodpage.component';

const routes: Routes = [
  {
    path: '',
    component: PublicPagesComponent,
    children: [
      { path: '', component: HomepageComponent },
      { path: 'organizers', component: OrganizerspageComponent },
      { path: 'hoods', component: HoodspageComponent },
      { path: 'hoods/:id', component: HoodpageComponent },
    ],
  },
];

@NgModule({
  declarations: [],
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule],
})
export class PublicPagesRoutingModule {}
