import { Injectable } from "@angular/core";
import { Subject } from 'rxjs'
import { HttpClient, HttpHeaders } from "@angular/common/http";
import { map } from 'rxjs/operators'
import { Router } from "@angular/router";
import { environment } from "src/environments/environment";


const BACKEND_URL =  environment.apiUrl;

@Injectable({
    providedIn: 'root'
})
export class DashboardService{

    constructor(private http: HttpClient, private router: Router) {}

    


    predict(file: File, days: string){

        const token = localStorage.getItem('access_token')

        const headers = new HttpHeaders({
            "Authorization": `Bearer ${token}`
        })

        console.log(file);
        let options = {"headers": headers}
        

        let postData = new FormData();

        postData.set('file', file);
        postData.set('days', days);

        console.log(postData.get("file"));
        

        this.http.post<any>(BACKEND_URL+"/predict", postData)
        .subscribe((response) => {
            console.log(response);
            
        })
    }

}