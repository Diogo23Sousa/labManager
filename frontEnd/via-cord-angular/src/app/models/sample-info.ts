export class SampleInfo {
    id: number;
    sampleId: string;
    labelingDate: string;
    labelingTime: string;
    initialWeight: number;
    bufferVolume: number;
    unitAgeUponLabeling: string;
    birthOrderReceivedMins: string;
    hospitalMins: string;
    hospitalTemp: string;
    originCourierMins: string;
    avgOriginCourierTemp: string;
    stdOriginCourierTemp: string;
    avgOriginCourierHumid: string;
    stdOriginCourierHumid: string;
    destinationCourierMins: string;
    avgDestinationCourierTemp: string;
    stdDestinationCourierTemp: string;
    avgDestinationCourierHumid: string;
    stdDestinationCourierHumid: string;
    planeMins: string;
    planeTemp: string;

    
    constructor(id: number, sampleId: string, labelingDate: string, labelingTime: string, initialWeight: number, bufferVolume: number, unitAgeUponLabeling: string, birthOrderReceivedMins: string, hospitalMins: string, hospitalTemp: string, originCourierMins: string, 
        avgOriginCourierTemp: string, stdOriginCourierTemp: string, avgOriginCourierHumid: string, stdOriginCourierHumid: string, destinationCourierMins: string, avgDestinationCourierTemp: string, stdDestinationCourierTemp: string, 
        avgDestinationCourierHumid: string, stdDestinationCourierHumid: string, planeMins: string, planeTemp: string) {
            this.id = id;
            this.sampleId = sampleId;
            this.labelingDate = labelingDate;
            this.labelingTime = labelingTime;
            this.initialWeight = initialWeight;
            this.bufferVolume = bufferVolume;
            this.unitAgeUponLabeling = unitAgeUponLabeling;
            this.birthOrderReceivedMins = birthOrderReceivedMins;
            this.hospitalMins =  hospitalMins;
            this.hospitalTemp = hospitalTemp;
            this.originCourierMins = originCourierMins;
            this.avgOriginCourierTemp = avgOriginCourierTemp;
            this.stdOriginCourierTemp = stdOriginCourierTemp;
            this.avgOriginCourierHumid = avgOriginCourierHumid;
            this.stdOriginCourierHumid = stdOriginCourierHumid;
            this.destinationCourierMins = destinationCourierMins
            this.avgDestinationCourierTemp = avgDestinationCourierTemp;
            this.stdDestinationCourierTemp = stdDestinationCourierTemp;
            this.avgDestinationCourierHumid = avgDestinationCourierHumid;
            this.stdDestinationCourierHumid = stdDestinationCourierHumid;
            this.planeMins = planeMins;
            this.planeTemp = planeTemp;
        }
    }