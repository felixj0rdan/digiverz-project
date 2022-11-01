import { HttpClient, HttpHeaders } from "@angular/common/http";
import { Injectable } from "@angular/core";
import { Router } from "@angular/router";
import { Subject } from "rxjs";

import { AuthData } from "./auth-data.model";
import { environment } from "src/environments/environment";


const BACKEND_URL =  environment.apiUrl + "/user/";


@Injectable({
    providedIn: 'root'
})
export class AuthService {
    private isAuthenticated = false;
    private access_token="";
    private refresh_token="";
    private tokenTimer: any;
    private userId="";
    private authStatusListener = new Subject<boolean>();

    constructor(private http: HttpClient, private router: Router) {}

    getAccessToken() {
        return this.access_token;
    }

    getRefreshToken() {
        return this.refresh_token;
    }

    getIsAuth() {
        // return this.isAuthenticated;
        return this.getAuthData();
    }

    getAuthStatusListener() {
        return this.authStatusListener.asObservable();
    }

    getUserId() {
        return this.userId;
    }

    createUser(email: string, password: string) {
        const authData: AuthData = {email: email, password: password};
        return this.http.post<any>(BACKEND_URL + 'signup', authData)
        .subscribe(response => {
            if(response.message === "User already exists."){
                alert(response.message)
            } 
            else
            this.router.navigate(['/auth/login']);
        }, error => {
            alert("Error")
            this.authStatusListener.next(false);
        });
    }

    login(email: string, password: string) {
        const authData: AuthData = {email: email, password: password};
        
        this.http.post<any>(BACKEND_URL + 'login', authData)
        .subscribe(response => {
            const access_token = response.access_token;
            this.access_token = access_token;
            this.refresh_token = response.refresh_token;
            
            if(access_token){
                this.isAuthenticated = true;
                this.userId = response.user_id;
                this.authStatusListener.next(true);           
                this.saveAuthData(access_token, this.refresh_token, this.userId)
                this.router.navigate(['/dashboard']);
            }
        }, error => {
            alert("Incorrect credentials")
            this.authStatusListener.next(false);
        });
    }

    autoAuthUser() {
        const authInformation = this.getAuthData();
        if(!authInformation){
            return;
        }

        const headers = new HttpHeaders({
            "Authorization": `Bearer ${authInformation.refresh_token}`
        })

        this.http.get<any>(BACKEND_URL + 'login', {headers: headers})
        .subscribe(response => {
            const access_token = response.access_token;
            this.access_token = access_token;
            this.refresh_token = response.refresh_token;
            
            if(access_token){
                this.isAuthenticated = true;
                this.userId = response.user_id;
                this.authStatusListener.next(true);         
                this.saveAuthData(access_token, this.refresh_token, this.userId)
                this.router.navigate(['/dashboard']);
            }
        }, error => {
            this.authStatusListener.next(false);
        });
    }

    logout() {
        this.access_token = "";
        this.refresh_token = "";
        this.isAuthenticated = false;
        this.authStatusListener.next(false);
        clearTimeout(this.tokenTimer);
        this.userId = "";
        this.clearAuthData();
        this.router.navigate(['/']);
    }


    private saveAuthData(access_token: string, refresh_token: string, userId: string) {
        localStorage.setItem('access_token', access_token);
        localStorage.setItem('refresh_token', refresh_token);
        localStorage.setItem('userId', userId);
        localStorage.setItem('logged_in', "true");
    }

    private clearAuthData() {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        localStorage.removeItem('userId');
        localStorage.removeItem('logged_in')
    }

    private getAuthData() {
        const access_token = localStorage.getItem('access_token');
        const refresh_token = localStorage.getItem('refresh_token');
        const userId = localStorage.getItem('userId');
        if(!access_token || !refresh_token){
            return;
        }

        return {
            access_token: access_token,
            refresh_token: refresh_token,
            userId: userId,
            loggend_in: localStorage.getItem('logged_in')
        }
    }

}