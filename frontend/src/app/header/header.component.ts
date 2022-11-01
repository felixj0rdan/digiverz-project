import { Component, OnDestroy, OnInit } from "@angular/core";
import { Subscription } from "rxjs";

import { AuthService } from "../auth-demo/auth.service";

@Component({
    selector: 'app-header',
    templateUrl: './header.component.html',
    styleUrls: ['./header.component.css']
})
export class HeaderComponent implements OnInit, OnDestroy {
    userIsAuthenticated = false;
    private authListenerSubs = new Subscription;

    constructor(private authService: AuthService) { }
    
    ngOnInit(): void {
        if(this.authService.getIsAuth()?.loggend_in === "true")
            this.userIsAuthenticated = true;
        else
            this.userIsAuthenticated = false;
        
    }

    onLogout() {
        this.authService.logout();
    }

    ngOnDestroy(): void {
        // this.authListenerSubs.unsubscribe();
    }
}