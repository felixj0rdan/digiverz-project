import { Component, OnInit } from '@angular/core';
import { FormControl, FormGroup, Validators } from "@angular/forms";
import { DashboardService } from './dashboard.service';
import { mimeType } from "./mime-type.validator";

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css']
})
export class DashboardComponent implements OnInit {

  filePreview="";
  isLoading = false;
  form!: FormGroup;
  file: any;
  days: any;

  constructor(private dashboardService: DashboardService) { }

  ngOnInit(): void {

    this.form = new FormGroup({
      'days': new FormControl(null, { validators: [Validators.required] }),
      'file': new FormControl(null, { validators: [Validators.required], asyncValidators: [mimeType]})
  })
  }

  onFilePicked(event: Event) {

    const file: any = (event.target as HTMLInputElement).files?.[0];
    // const file = event.target.files[0]
    

    this.file = file
    
    this.form.patchValue({ 'file': file });
    this.form.get('file')?.updateValueAndValidity();
    
    const reader = new FileReader();
    reader.onload = () => {
        this.filePreview = reader.result as string;
    };
    reader.readAsDataURL(file);
}


onPredict() {
  
  console.log(this.form);
  // if (this.form.invalid)
  //     return;
  console.log(this.days);
  
  this.isLoading = true;
  // if (this.mode === 'create') {
  //     this.postsService.addPost(this.form.value.title, this.form.value.content, this.form.value.image)
  // } else {
  //     this.postsService.updatePost(
  //         this.postId,
  //         this.form.value.title,
  //         this.form.value.content,
  //         this.form.value.image
  //     )
  // }
  this.dashboardService.predict(this.file, this.days)

  this.form.reset();
}

onDaysPicked(event: Event){
  // this.days = document.getElementById('days')
  // console.log(val);
  this.days = (event.target as HTMLInputElement).value
  
}


}

// --------------------------------------------------------------------------------------------------------------------------------------------------------------

// import { Component, OnInit } from '@angular/core';
// // import { AuthenticationService } from 'src/app/services/authentication.service';
// import { HttpClientModule } from '@angular/common/http';
// import { HttpClient, HttpHeaders } from '@angular/common/http'
// // import { HotToastService } from '@ngneat/hot-toast';

// @Component({
//   selector: 'app-dashboard',
//   templateUrl: './dashboard.component.html',
//   styleUrls: ['./dashboard.component.css']
// })
// export class DashboardComponent implements OnInit {
 


//   // user$ = this.authService.currentUser$;

//   constructor(
//     // private authService: AuthenticationService,
//     // private http: HttpClientModule,
//     private http: HttpClient,
//     // private toast: HotToastService,

//     ) { }

//   ngOnInit(): void {
//   }
//   file:any;
//   days: any;
//   getFile(event:any){
//     this.file=event.target.files[0];
//     console.log("file",this.file)

//   }
//   onDaysPicked(event:any){
//     this.days=event.target.value;
//     console.log("days",this.days)

//   }
//   submitData(){

//     const token = localStorage.getItem('access_token')

//     // const headers = new HttpHeaders({
//     //       'Content-Type': 'multipart/form-data'
//     //   })

//     console.log(token);
    

//     let formData = new FormData();
//     formData.set("file",this.file)
//     formData.set("days",this.days)

//     // console.log(formData.forEach);
//     formData.forEach((element: any) => {
//       console.log(element);
      
//     });
    

//     this.http.post<any>("http://127.0.0.1:5000/api/predict",formData)
//     .subscribe((response)=>
//     {
//       console.log(response)
//     })
//   }
 
 
//     }
