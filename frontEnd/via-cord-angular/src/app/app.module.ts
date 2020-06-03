import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { HomePageComponent } from './components/home-page.component';
import { MatFormFieldModule, MatFormFieldControl} from '@angular/material/form-field';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { FormsModule } from '@angular/forms';
import {MatDatepickerModule} from '@angular/material/datepicker';
import { MatNativeDateModule } from '@angular/material/core';
import {MatTabsModule} from '@angular/material/tabs';
import { AddSampleTabComponent } from './components/add-sample-tab/add-sample-tab.component';
import { CurrentSamplesTabComponent } from './components/current-samples-tab/current-samples-tab.component';
import { EditSampleTabComponent } from './components/edit-sample-tab/edit-sample-tab.component';
import { ProcessedSamplesService } from './services/processedsamples.service';
import { SampleInfoService } from './services/sampleinfo.service';
import {MatDialogModule} from '@angular/material/dialog';
import {MatInputModule} from '@angular/material/input';
import { DatePipe } from '@angular/common';
import { HttpClientModule } from '@angular/common/http';


@NgModule({
  declarations: [
    AppComponent,
    HomePageComponent,
    AddSampleTabComponent,
    CurrentSamplesTabComponent,
    EditSampleTabComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    MatFormFieldModule,
    BrowserAnimationsModule,
    FormsModule,
    MatDatepickerModule,
    MatNativeDateModule,
    MatTabsModule,
    MatDialogModule,
    MatInputModule,
    HttpClientModule
  ],
  providers: [ProcessedSamplesService, SampleInfoService, DatePipe],
  bootstrap: [AppComponent]
})
export class AppModule { }
