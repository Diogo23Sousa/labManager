import json

from flask import Blueprint, request

from viacord.main.business.ProcessedSamplesBusiness import ProcessedSamplesBusiness
from viacord.main.repositories.SampleInfoRepository import SampleInfoRepository

# BLUEPRINT (sample_info_controller)
sample_info_controller = Blueprint('sample_info_controller', __name__, template_folder='templates')

# APPLICATION ROUTES


# SAMPLE INFORMATION - GET ALL
@sample_info_controller.route('/sampleinfo/getall', methods=['GET'])
def getAllSampleInfo():
    return json.dumps(SampleInfoRepository.getAllSampleInfo(), default=lambda x: x.__dict__)


# SAMPLE INFORMATION - GET BY ID
@sample_info_controller.route('/sampleinfo/get/id/<id>', methods=['GET'])
def getSampleInformationById(id):
    return json.dumps(SampleInfoRepository.getSampleBySampleID(id), default=lambda x: x.__dict__)


# SAMPLE INFORMATION - GET BY SAMPLE ID
@sample_info_controller.route('/sampleinfo/get/sampleid/<sampleId>', methods=['GET'])
def getSampleInformationBySampleId(sampleId):
    return json.dumps(SampleInfoRepository.getSampleBySampleID(sampleId), default=lambda x: x.__dict__)


# SAMPLE INFORMATION - GET BY DATE
@sample_info_controller.route('/sampleinfo/get/date/<sampleDate>', methods=['GET'])
def getProcessedSampleByDate(sampleDate):
    return json.dumps(SampleInfoRepository.getAllSampleInfoByDate(sampleDate), default=lambda x: x.__dict__)


# SAMPLE INFORMATION - UPDATE SAMPLE INFO
@sample_info_controller.route('/sampleinfo/calculate', methods=['POST'])
def calculateBufferVolume():
    correctJSONContent = str(request.json).replace("\'", "\"")
    return ProcessedSamplesBusiness.calculateBufferVolume(correctJSONContent)
