import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { AuthGuard } from "./auth-demo/auth.guard";
import { DashboardComponent } from './dashboard/dashboard.component';

const routes: Routes = [
  { path: "auth", loadChildren: () => import('./auth-demo/auth.module').then( m => m.AuthModule) },
  { path: "dashboard", component: DashboardComponent }

]


@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule],
  providers: [AuthGuard]
})
export class AppRoutingModule { }
