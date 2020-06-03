export class ProcessedSample {
    id: number
    sampleId: string;
    isWeightKnown: string;
    initialWeight: number;
    sampleDate: string;
    comments: string;
    bufferVolume: number;

    constructor(id: number, sampleId: string, isWeightKnown: string, initialWeight: number, sampleDate: string, comments: string, bufferVolume: number) {
        this.id = id;
        this.sampleId = sampleId;
        this.isWeightKnown = isWeightKnown;
        this.initialWeight = initialWeight;
        this.sampleDate = sampleDate;
        this.comments = comments;
        this.bufferVolume = bufferVolume;
    }
}