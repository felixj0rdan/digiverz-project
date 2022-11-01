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

    


    predict(file: File, duration: number, periodicity: string){

        const token = localStorage.getItem('access_token')

        const headers = new HttpHeaders({
            "Authorization": `Bearer ${token}`
        })

        let options = {"headers": headers}
        let days:number = 0;
        let postData = new FormData();

        postData.set('file', file);
        postData.set('duration', duration+"");
        postData.set('periodicity', periodicity);

        return this.http.post<any>(BACKEND_URL+"/predict", postData)
    }

}