import { Component, OnDestroy, OnInit } from '@angular/core';
import { FormControl, FormGroup, Validators } from "@angular/forms";
import { DashboardService } from './dashboard.service';
import { mimeType } from "./mime-type.validator";
import Chart from 'chart.js/auto';
import { Router } from '@angular/router';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css']
})
export class DashboardComponent implements OnInit, OnDestroy {

  filePreview="";
  isLoading = false;
  form!: FormGroup;
  file: any;
  filename = "";
  duration: any;
  periodicity='days';
  public predictionChart: any;
  public errorChart: any;
  metrics: any;
  ctx: any;

  constructor(private dashboardService: DashboardService,private router: Router) { }
  ngOnDestroy(): void {
    
  }

  ngOnInit(): void {

    let loggedIn = localStorage.getItem('logged_in')
    if(!loggedIn || loggedIn !== "true"){
      this.router.navigate(['/'])
    }

    this.form = new FormGroup({
      'duration': new FormControl(null, { validators: [Validators.required] }),
      'file': new FormControl(null, { validators: [Validators.required], asyncValidators: [mimeType]}),
      'periodicity': new FormControl(null, { validators: [Validators.required] }),
  })
  }

  onFilePicked(event: Event) {

    const file: any = (event.target as HTMLInputElement).files?.[0];  

    this.file = file
    this.filename = file.name
    
    
    this.form.patchValue({ 'file': file });
    this.form.get('file')?.updateValueAndValidity();
    
    const reader = new FileReader();
    reader.onload = () => {
        this.filePreview = reader.result as string;
    };
    reader.readAsDataURL(file);
}
removeFile(){
  this.file = null
  this.filename = ""
}


onPredict() {

  if(!this.file || !this.duration || !this.periodicity){
    alert("Please enter all the required details.")
    return;
  }
  
  
  this.isLoading = true;
  this.dashboardService.predict(this.file, this.duration, this.periodicity)
  .subscribe((response) => {
      this.isLoading = false;
      this.metrics = response;   
      
      this.createPredictionChart(response)
      this.createErrorChart(response.error_data.datetime, response.error_data.error)
      
  })

  this.form.reset();
  this.periodicity='days';
}


onDurationPicked(event: Event){
  this.duration = (event.target as HTMLInputElement).value
}
createPredictionChart(response: any){
  let buffer:any = []
  for(let i=0; i<response.train_data.Sales.length; i++){
    buffer[i] = null
  }
  let yax = buffer.concat(response.pred_data.Sales)
  if(this.predictionChart)
    this.predictionChart.destroy()
  
  this.predictionChart = new Chart("PredictionChart", {
    type: 'line', 

    data: {
      labels: response.x, 
      datasets: [
      {
        label: "Past Sales",
        data: response.train_data.Sales,
        backgroundColor: "blue"

      },
      {
        label: `Future Sales (for ${response.duration+" "+response.periodicity})`,
        data: yax,
        backgroundColor: 'limegreen',
      }  
    ]
    },
    
    options: {
      aspectRatio:2.5,
      responsive: true,
      interaction: {
        mode: 'index',
        intersect: false,
      },
      plugins: {
        title: {
            display: true,
            text: `Predicted Sales`,
            font: {
              size: 30
            }
        }
    }
    }
    
  });

}

createErrorChart(datetime: any, error:any){

  if(this.errorChart)
    this.errorChart.destroy()
  
  this.ctx = document.getElementById('ErrorChart');
  
  this.errorChart = new Chart(this.ctx, {
    type: 'bar', 

    data: {
      labels: datetime, 
      datasets: [
      {
        label: "Variance",
        data: error,
        backgroundColor: "blue"

      }
    ]
    },
    
    options: {
      aspectRatio:2.5,
      responsive: true,
      interaction: {
        mode: 'index',
        intersect: false,
      },
      plugins: {
        title: {
            display: true,
            text: 'Test Prediction vs Actual Sales Variance Graph',
            font: {
              size: 20
            }
        }
    }
    }
    
  });

}


}

