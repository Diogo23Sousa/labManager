class ProcessedSample:
    def __init__(self,id, sampleId,  isWeightKnown, initialWeight, sampleDate, comments, bufferVolume):
        self.id = id;
        self.sampleId = sampleId
        self.isWeightKnown = isWeightKnown
        self.initialWeight = initialWeight
        self.sampleDate = sampleDate
        self.comments = comments
        self.bufferVolume = bufferVolume