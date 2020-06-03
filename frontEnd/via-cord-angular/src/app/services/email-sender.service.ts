import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { ProcessedSample } from '../models/processed-sample';

const httpOptions = {
  headers: new HttpHeaders({ 'Content-Type': 'application/json' })
};

@Injectable({
  providedIn: 'root'
})

export class EmailSenderService {

private sampleUrl: string;
 
  constructor(private httpClient: HttpClient) {
    this.sampleUrl =  'http://localhost:5000';
  }

  public sendEmail(emailToSend, processedSamples) {
    return this.httpClient.post<ProcessedSample[]>(this.sampleUrl.concat('/sendemail/' + emailToSend), JSON.stringify(processedSamples), httpOptions); 
  }
}