import { Component, OnDestroy, OnInit } from "@angular/core";
import { NgForm, NgModel } from "@angular/forms";
import { Router } from "@angular/router";
import { Subscription } from "rxjs";
import { AuthService } from "../auth.service";

@Component({
    templateUrl: './signup.component.html',
    styleUrls: ['./signup.component.css']
})
export class SignupComponent implements OnInit, OnDestroy {
    isLoading = false;
    private authStatusSub!: Subscription;
    notsame = false;
    public password = ""

    constructor(public authService: AuthService, private router: Router ) {}
    
    ngOnInit(): void {
        this.notsame = false;
        this.authStatusSub = this.authService.getAuthStatusListener().subscribe(
            authStatus => {
                this.isLoading = false;
            }
        );
    }

    onSignup(form: NgForm){

        if(form.invalid){
            return;
        }
        if(form.value.password !== form.value.repassword){
            alert("Passwords don't match.")
            return;
        }

        this.isLoading = true;
        this.authService.createUser(form.value.email, form.value.password)
        
        
    } 
    onPassword(pw: NgModel){
        this.password = pw.value
    }
    secondEntry(passwordsec: NgModel){
        if(this.password !== passwordsec.value){
            this.notsame = true;
        } else {
            this.notsame = false;
        }

    }

    ngOnDestroy(): void {
        this.authStatusSub.unsubscribe();
    }
}