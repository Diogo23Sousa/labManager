import { Component, OnInit, Injectable } from '@angular/core';
import { DatePipe } from '@angular/common';
import { ProcessedSamplesService } from 'src/app/services/processedsamples.service';
import { ProcessedSample } from 'src/app/models/processed-sample';

@Component({
  selector: 'app-edit-sample-tab',
  templateUrl: './edit-sample-tab.component.html',
  styleUrls: ['./edit-sample-tab.component.css']
})
@Injectable()
export class EditSampleTabComponent implements OnInit {
// MY FORM DATA
id;
sampleIdtoUpdate;
isInitialWeightKnown = 'true'
initialWeight : number;
currentDate = this.datepipe.transform(Date.now(), 'MM-dd-yyyy');
choosenDate = this.currentDate;
comments = '';
bufferVolume: number;

// MY AVAILABLE SAMPLE
myProcessedSamples = []

// Variables used to provided dinamic messages
sampleIdIsNotValid = 'none';
initialWeightIsNotValid = 'none';
bufferVolumeIsNotValid = 'none';
samplesWasUpdated = 'none';
samplesWasNotUpdated = 'none';
sampleWasDeleted = 'none';

constructor(public datepipe: DatePipe, public processedSamplesService : ProcessedSamplesService) { }

// GET ALL PROCESSSED SAMPLES AVAILABLE - ON INIT
ngOnInit() {
  this.getAllProcessedSamples()
}

// GET ALL - PROCESSED SAMPLES
getAllProcessedSamples() {
  this.processedSamplesService.findAll().subscribe(allProcessedSamples => {
    allProcessedSamples.forEach(processedSample => {
        this.myProcessedSamples.push(JSON.parse(JSON.stringify(processedSample)))
      })
  })
}

// THE FORM IS UNLOCKED IF THE SAMPLE IS SELECTED
selectSampleToEdit () {
    this.processedSamplesService.findBySampleId(this.sampleIdtoUpdate).subscribe(mySampleToEdit => {
      this.id = mySampleToEdit.id
      this.initialWeight = mySampleToEdit.initialWeight;
      this.comments = mySampleToEdit.comments;
      this.choosenDate = this.currentDate = mySampleToEdit.sampleDate;
      this.bufferVolume = mySampleToEdit.bufferVolume;
    })
    document.getElementById("weightSection").removeAttribute("disabled");
    document.getElementById("bufferSection").removeAttribute("disabled");
    document.getElementById("commentSection").removeAttribute("disabled");
    document.getElementById("updateButton").removeAttribute("disabled");
    document.getElementById("clearButton").removeAttribute("disabled");
}


// SENDSAMPLEINFORMATION() -> WILL EVALUATE THE FORM INPUTS AND HELP THE USER IF THERE ARE ERRORS
sendSampleInformation() {
  //IF BUFFER VOLUME IS WRONG AND WEIGHT FIELDS ARE CORRECT
  if (isNaN(this.bufferVolume) || (this.bufferVolume == 0)) {
    if (!isNaN(this.initialWeight)) {
      this.initialWeightIsNotValid = '';
    }
    this.bufferVolumeIsNotValid = this.samplesWasNotUpdated = '';
    this.samplesWasUpdated = 'none'; 
  }
  //IF WEIGHT FIELDS ARE WRONG AND BUFFER VOLUME IS CORRECT
  if (isNaN(this.initialWeight) || (this.initialWeight == 0)) {
    if (!isNaN(this.bufferVolume)) {
      this.bufferVolumeIsNotValid = ''
    }
    this.initialWeightIsNotValid = this.samplesWasNotUpdated = '';
    this.samplesWasUpdated = 'none';
  }
  // IF SAMPLE ID and WEIGHT FIELDS ARE CORRECT THE REQUEST IS SENT
  else {
    this.comments = this.comments.replace("'"," ")
    if (this.comments.includes('"')) {this.comments = 'Comment char not valid.'}
    this.updateSampleInformation()   
  }
}


// AFTER THE FORM IS VALIDATED THE SAMPLE IS UPDATED
updateSampleInformation() {
  let myProcessedSample = new ProcessedSample(this.id,this.sampleIdtoUpdate, this.isInitialWeightKnown,  this.initialWeight, this.datepipe.transform(this.choosenDate, 'MM-dd-yyyy'), this.comments, this.bufferVolume);
  this.processedSamplesService.editSample(myProcessedSample).subscribe(updateSample => console.log(updateSample))
  
  // Update the messages
  this.sampleIdIsNotValid = this.initialWeightIsNotValid = this.bufferVolumeIsNotValid = this.samplesWasNotUpdated= 'none';
  this.samplesWasUpdated = '';

  // Reset the form to avoid consecutive calls
  document.getElementById("weightSection").setAttribute("disabled", "true");
  document.getElementById("bufferSection").setAttribute("disabled", "true");
  document.getElementById("commentSection").setAttribute("disabled", "true");
  document.getElementById("updateButton").setAttribute("disabled", "true");
  document.getElementById("clearButton").setAttribute("disabled", "true");
  setTimeout( () => {location.reload()}, 1000 );
}

// DELETE THE CURRENT CHOOSEN SAMPLE
deleteSample() {
  this.processedSamplesService.deleteBySampleId(this.sampleIdtoUpdate).subscribe(sampleToDelete => console.log(sampleToDelete));
  this.sampleWasDeleted = '';
  this.samplesWasUpdated = this.samplesWasNotUpdated = 'none';
  setTimeout( () => {location.reload()}, 1000 );
}
}
