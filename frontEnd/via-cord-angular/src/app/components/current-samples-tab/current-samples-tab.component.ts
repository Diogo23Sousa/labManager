import { Component, OnInit } from '@angular/core';
import { DatePipe } from '@angular/common';
import { ProcessedSamplesService } from 'src/app/services/processedsamples.service';
import { ExcelService } from 'src/app/services/excel.service';
import { ProcessedSample } from 'src/app/models/processed-sample';
import { EmailSenderService } from 'src/app/services/email-sender.service';

@Component({
  selector: 'app-current-samples-tab',
  templateUrl: './current-samples-tab.component.html',
  styleUrls: ['./current-samples-tab.component.css']
})
export class CurrentSamplesTabComponent implements OnInit {
// FROM DATA - DEFAULT VALUE
totalSamplesAdded: number = 0;
totalBufferVolume: number = 0;
totalAliquotsNeeded: number = 0;
bufferLeftover: number = 0;
emailToSend = '';
totalProcessedSamples= [];
currentDate = this.datepipe.transform(Date.now(), 'MM-dd-yyyy');
choosenDate = this.currentDate;

// DINAMIC MESSAGES TO HELP THE USER
emailIsNotValid = 'none';
emailWasSent = 'none';

constructor(public datepipe: DatePipe, public processedSamplesService: ProcessedSamplesService, public excelService: ExcelService, public emailSenderService: EmailSenderService) { }

ngOnInit() {
}

// GET ALL PROCESSED SAMPLES BY DATE - REQUEST IS PERFORMED ON INIT
ngAfterViewInit() {
  this.getAllProcessedSamplesByDate(this.choosenDate)
}

// GET ALL PROCESSED SAMPLES BY DATE
getAllProcessedSamplesByDate(date) {
  this.processedSamplesService.findByDate(date).subscribe(allProcessedSamples => {
    this.totalProcessedSamples = [];
    this.totalBufferVolume = this.totalSamplesAdded = this.totalAliquotsNeeded = this.bufferLeftover = 0;
    allProcessedSamples.forEach(processedSample => {
        this.totalBufferVolume += +processedSample.bufferVolume;
        this.totalSamplesAdded++
        this.totalProcessedSamples.push(JSON.parse(JSON.stringify(processedSample)))
      })
  })
  setTimeout( () => {
    this.totalAliquotsNeeded =  Math.ceil(this.totalBufferVolume/40);
    this.bufferLeftover = (this.totalAliquotsNeeded*40 - this.totalBufferVolume)
  }, 500 );
}

// GET ALL PROCESSED SAMPLES BY DATE - THE USER CHOOSES THE DATE -> getAllProcessedSamplesByDate() is called.
changeDate() {
  this.getAllProcessedSamplesByDate(this.datepipe.transform(this.choosenDate, 'MM-dd-yyyy'));
}

// GENERATE CSV FILE WITH THE CURRENT INFORMATION
generateReport() {
  let listToExport = this.totalProcessedSamples;
  listToExport.push(new ProcessedSample(this.totalSamplesAdded, " " , " ", 0, " ", "Aliquots: ".concat(this.totalAliquotsNeeded.toString()), this.totalBufferVolume))
  this.excelService.exportAsExcelFile(listToExport, 'TotalProcesedSamples'.concat(this.datepipe.transform(this.choosenDate, 'MM-dd-yyyy')));
 
}

// SEND THE INFORMATION VIA EMAIL
sendMeThisInformation(){
  if (this.emailToSend == '' || !this.emailToSend.includes('@') || this.emailToSend.length < 4) {
    this.emailIsNotValid = '';
  } else {
    let myMessage = "On the " + this.choosenDate + " were processed " + this.totalSamplesAdded + " Samples with a total of " + 
    this.totalBufferVolume + " mL of EDB buffer volume needed. In order to process all of this samples the technicians will need: " +
    this.totalAliquotsNeeded + " Aliquots of Buffer EDB (40mL each)."
    this.emailSenderService.sendEmail(this.emailToSend, myMessage).subscribe(emailToSend => console.log(emailToSend))
    this.emailIsNotValid = 'none';
    this.emailWasSent = '';
  }
}
}