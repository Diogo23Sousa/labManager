import { Component, OnInit, Injectable } from '@angular/core';
import { DatePipe } from '@angular/common';
import { SampleInfoService} from '../../services/sampleinfo.service'
import { SampleInfo } from 'src/app/models/sample-info';
import { ProcessedSamplesService } from 'src/app/services/processedsamples.service';
import { ProcessedSample } from 'src/app/models/processed-sample';
import { Router } from '@angular/router';

@Component({
  selector: 'app-add-sample-tab',
  templateUrl: './add-sample-tab.component.html',
  styleUrls: ['./add-sample-tab.component.css']
})
@Injectable()
export class AddSampleTabComponent implements OnInit {

// Variables used in the NGMODEL
sampleID = '';
isWeightKnown = 'false';
initialWeight: number = 0;
comments = '';

// Variables used to retrieve the information from the different SERVICES
mySampleInfoList = [];
mySampleInfo : SampleInfo;
currentDate = this.datepipe.transform(Date.now(), 'MM-dd-yyyy');
choosenDate = this.currentDate;
myProcessedSampleId;


// Variables used to provided DINAMIC MESSAGES to help the user fill the form
sampleIdIsNotValid = '';
initialWeightIsNotValid = 'none';
sampleWasAdded = 'none';
sampleWasNotAdded = 'none';
sampleWasAlreadyProcessed = 'none';


constructor(public datepipe: DatePipe, public sampleInfoService: SampleInfoService, public processedSamplesService: ProcessedSamplesService, public router: Router) { }

ngOnInit() {}

ngAfterViewInit() {
this.getAllSampleInfoByDate(this.choosenDate)
}

// GET ALL - SAMPLE INFORMATION
getAllSampleInfo(){
  this.sampleInfoService.findAll().subscribe(allSampleInformation => {
    allSampleInformation.forEach(sampleInfo => {
        this.mySampleInfoList.push(JSON.parse(JSON.stringify(sampleInfo)))
      })
  })
}

// GET SAMPLE BY DATE (DEFAULT DATE) - SAMPLE INFORMATION 
getAllSampleInfoByDate(date) {
  this.sampleInfoService.findByDate(date).subscribe(allSampleInformationByDate => {
    // RESET THE SAMPLE INFO LIST BEFORE THE SUBSCRIPTION
    this.mySampleInfoList = []
    allSampleInformationByDate.forEach(sampleInfo => {
        this.mySampleInfoList.push(JSON.parse(JSON.stringify(sampleInfo)))
      })
  })
}

// GET SAMPLE BY DATE (CHOOSEN DATE) - SAMPLE INFORMATION  
changeDate() {
  this.getAllSampleInfoByDate(this.datepipe.transform(this.choosenDate, 'MM-dd-yyyy'));
}

// GET SAMPLE BY SAMPLEID - SAMPLE INFORMATION
selectSampleId() {
  this.sampleInfoService.findSampleBySampleId(this.sampleID).subscribe(sample => {
    this.mySampleInfo = sample;
  })
  // GET SAMPLE BY SAMPLEID - PROCESSED SAMPLE -> CHECK IF THE SAMPLE WAS ALREADY PROCESSED 
  this.processedSamplesService.findBySampleId(this.sampleID).subscribe(processedSample => {
    this.myProcessedSampleId = processedSample.id;
  })
}

// IF THE USER KNOWNS THE WEIGHT -> ENABLE initialWeight input
checkIfWeightIsKnows () {
  if (this.isWeightKnown == 'true') {
    document.getElementById("valueForInput").removeAttribute("disabled");
    } else {
    document.getElementById("valueForInput").setAttribute("disabled", "true");
  }
}

// SENDSAMPLEINFORMATION() -> WILL EVALUATE THE FORM INPUTS AND HELP THE USER IF THERE ARE ERRORS
sendSampleInformation() {
    //IF SAMPLE ID IS WRONG AND WEIGHT FIELDS ARE CORRECT
    if (this.sampleID === '' || !this.sampleID.includes('-')) {
      if (this.isWeightKnown === 'true' && !isNaN(this.initialWeight)) {this.initialWeightIsNotValid = '';}
      this.sampleIdIsNotValid = this.sampleWasNotAdded = '';
      this.sampleWasAdded = 'none';
    }
    //IF SAMPLE ID IS CORRECT AND WEIGHT FIELDS ARE WRONG
    if (this.isWeightKnown === 'true' && (isNaN(this.initialWeight) || (this.initialWeight == 0))) {
      if (this.sampleID !== '' || this.sampleID.includes('-')) {
        this.sampleIdIsNotValid = ''
      }
      this.initialWeightIsNotValid = this.sampleWasNotAdded = '';
      this.sampleWasAdded = 'none';
    }

    // IF THE SAMPLE WAS ALREADY PROCESSED -> ERROR
    if (!isNaN(this.myProcessedSampleId)) {
        this.sampleWasAlreadyProcessed = this.sampleWasNotAdded = '';
        this.sampleWasAdded = 'none';
      }

    // IF SAMPLE ID IS CORRECT AND WEIGHT FIELDS ARE CORRECT, AND THE SAMPLE WAS NOT PROCESSED
    else {
      this.comments = this.comments.replace("'"," ")
      if (this.comments.includes('"')) {this.comments = 'Comment char not valid.'}
      // AFTER VALIDATION THE REQUEST IS SENT TO THE SERVICES
      this.sendMyValidatedSampleInformation()   
    }
}

  sendMyValidatedSampleInformation() {
  // CALCULATING BUFFER VOLUME BASED ON THE INITIAL WEIGHT AND SAMPLE INFORMATION - DEFAULT VALUE IS 27
  let bufferVolume;
  this.mySampleInfo.initialWeight = this.initialWeight
 
  // CALCULATE BUFFER VOLUME - AFTER THE USER CHOOSES THE INITIAL WEIGHT WE WILL CALCULATE AND UPDATE SAMPLE INFO
  this.sampleInfoService.calculateBufferVolume(this.mySampleInfo).subscribe(sampleToCalculate => {
    console.log(sampleToCalculate)
    bufferVolume = sampleToCalculate.bufferVolume
  })

  // NEW PROCESSED SAMPLE USING NEW VALUES - setTimeOut is used to wait for the data from the preview request (ASYNC)
  setTimeout(() => {
    let myProcessedSample = new ProcessedSample(0,this.mySampleInfo.sampleId,this.isWeightKnown,this.initialWeight, this.datepipe.transform(this.choosenDate, 'MM-dd-yyyy'), this.comments, bufferVolume)
    this.processedSamplesService.newSample(myProcessedSample).subscribe(submitNewSample => console.log(submitNewSample));
  },900)

  setTimeout(() => {                                                          
    location.reload()
  }, 1200)

  // UPDATE THE MESSSAGES
  this.initialWeightIsNotValid = this.sampleWasNotAdded = this.sampleWasAlreadyProcessed = 'none';
  this.sampleWasAdded = '';
  document.getElementById("valueForInput").setAttribute("disabled", "true");
}
}