import json

from flask import Blueprint, request

from viacord.main.repositories.ProcessedSamplesRepository import ProcessedSamplesRepository
from viacord.main.configuration.EmailSender import EmailSender

# BLUEPRINT (processed_sample_controller)
processed_samples_controller = Blueprint('processed_samples_controller', __name__, template_folder='templates')


# MAIN ROUTE
@processed_samples_controller.route('/', methods=['GET'])
def application_status():
    return '<h1> Controller is working. </h1>'


# MAIN ROUTE
@processed_samples_controller.route('/sendemail/<emailToSend>', methods=['POST'])
def send_mail(emailToSend):
    correctJSONContent = str(request.json).replace("\'", "\"")
    EmailSender.sendEmail(emailToSend, correctJSONContent)
    return "Email was sent"


# PROCESSED SAMPLES - GET ALL
@processed_samples_controller.route('/psamples/getall', methods=['GET'])
def getAllProcessedSamples():
    return json.dumps(ProcessedSamplesRepository.getAllProcessedSamples(), default=lambda x: x.__dict__)


# PROCESSED SAMPLES - GET BY ID
@processed_samples_controller.route('/psamples/get/id/<id>', methods=['GET'])
def getProcessedSampleById(id):
    return json.dumps(ProcessedSamplesRepository.getSampleBySampleID(id), default=lambda x: x.__dict__)


# PROCESSED  SAMPLES - GET BY SAMPLE ID
@processed_samples_controller.route('/psamples/get/sampleid/<sampleId>', methods=['GET'])
def getSampleInformationBySampleId(sampleId):
    return json.dumps(ProcessedSamplesRepository.getSampleBySampleID(sampleId), default=lambda x: x.__dict__)


# PROCESSED SAMPLES - GET BY DATE
@processed_samples_controller.route('/psamples/get/date/<sampleDate>', methods=['GET'])
def getProcessedSampleByDate(sampleDate):
    return json.dumps(ProcessedSamplesRepository.getAllProcessedSamplesByDate(sampleDate), default=lambda x: x.__dict__)


# PROCESSED SAMPLES - ADD NEW SAMPLE
@processed_samples_controller.route('/psamples/add', methods=['POST'])
def addNewProcessedSample():
    correctJSONContent = str(request.json).replace("\'", "\"")
    ProcessedSamplesRepository.newProcessedSample(correctJSONContent)
    return "Sample was added"


# PROCESSED SAMPLES - EDIT SAMPLE
@processed_samples_controller.route('/psamples/edit', methods=['POST'])
def editProcessedSample():
    correctJSONContent = str(request.json).replace("\'", "\"")
    ProcessedSamplesRepository.editProcessedSample(correctJSONContent)
    return "Sample was updated"


# PROCESSED SAMPLES - DELETE BY ID
@processed_samples_controller.route('/psamples/delete/sampleid/<sampleId>', methods=['DELETE'])
def deleteProcessedSampleBySampleId(sampleId):
    ProcessedSamplesRepository.deleteProcessedSampleBySampleId(sampleId)
    return "Sample was deleted."


# PROCESSED SAMPLES - DELETE ALL
@processed_samples_controller.route('/psamples/deleteall', methods=['DELETE'])
def deleteAllProcessedSample():
    ProcessedSamplesRepository.deleteAllProcessedSamples()
    return "Samples were deleted."