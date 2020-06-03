import { Injectable } from '@angular/core';
import { HttpHeaders, HttpClient } from '@angular/common/http';
import { SampleInfo } from '../models/sample-info';
import 'rxjs/Rx'
import { map } from 'rxjs-compat/operator/map';

const httpOptions = {
  headers: new HttpHeaders({ 'Content-Type': 'application/json' })
};

const httpOptions2: { headers; observe; } = {
  headers: new HttpHeaders({
    'Content-Type':  'application/json'
  }),
  observe: 'response' as 'body'
};


@Injectable({
  providedIn: 'root'
})
export class SampleInfoService {

private sampleUrl: string;
 
  constructor(private httpClient: HttpClient) {
    this.sampleUrl =  'http://localhost:5000/sampleinfo';
  }

  public findById(id: number) {
    return this.httpClient.get<SampleInfo>(this.sampleUrl.concat('/get/') + id);
  }
 
  public findAll() {
    return this.httpClient.get<SampleInfo[]>(this.sampleUrl.concat('/getall'));
  }

  public findSampleBySampleId(sampleId) {
    return this.httpClient.get<SampleInfo>(this.sampleUrl.concat('/get/sampleid/' + sampleId))
  }

  public findByDate(date: String) {
    return this.httpClient.get<SampleInfo[]>(this.sampleUrl.concat('/get/date/' + date)); 
  }

  public newSample (sample: SampleInfo) {
    return this.httpClient.post<SampleInfo>(this.sampleUrl.concat('/add'), JSON.stringify(sample), httpOptions);
  }

  public calculateBufferVolume(sampleInfo: SampleInfo) {
    return this.httpClient.post<SampleInfo>(this.sampleUrl.concat('/calculate') , JSON.stringify(sampleInfo), httpOptions);
}
}
