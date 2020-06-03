import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { ProcessedSample } from '../models/processed-sample';

const httpOptions = {
  headers: new HttpHeaders({ 'Content-Type': 'application/json' })
};


@Injectable({
  providedIn: 'root'
})
export class ProcessedSamplesService {

private sampleUrl: string;
 
  constructor(private httpClient: HttpClient) {
    this.sampleUrl =  'http://localhost:5000/psamples';
  }



 
  public findAll() {
    return this.httpClient.get<ProcessedSample[]>(this.sampleUrl.concat('/getall'));
  }

  public findBySampleId(sampleId) {
    return this.httpClient.get<ProcessedSample>(this.sampleUrl.concat('/get/sampleid/' + sampleId));
  }

  public findById(id) {
    return this.httpClient.get<ProcessedSample>(this.sampleUrl.concat('/get/id/' + id));
  }

  public findByDate(date) {
    return this.httpClient.get<ProcessedSample[]>(this.sampleUrl.concat('/get/date/' + date)); 
  }

  public newSample (processedSample: ProcessedSample) {
    return this.httpClient.post<ProcessedSample>(this.sampleUrl.concat('/add'), JSON.stringify(processedSample), httpOptions);
  }

  public editSample (processedSample: ProcessedSample) {
    return this.httpClient.post<ProcessedSample>(this.sampleUrl.concat('/edit'), JSON.stringify(processedSample), httpOptions);
  }

  public deleteBySampleId (sampleId: Number) {
  return this.httpClient.delete(this.sampleUrl.concat('/delete/sampleid/' + sampleId));  
  }

  public deleteAll () {
    return this.httpClient.delete(this.sampleUrl.concat('/deleteall'));
  }
}