import json
from flask import Blueprint

from viacord.main.configuration.Configuration import Configuration
from viacord.main.models.SampleInfo import SampleInfo

# BLUEPRINT (sample_info_repository)
sample_info_repository = Blueprint('sample_info_repository', __name__, template_folder='templates')


class SampleInfoRepository:
    def __init__(self):
        self = self


# GET ALL - SAMPLE INFO
    @staticmethod
    def getAllSampleInfo():
        myDBconnection = Configuration.openDBconnection()
        cursor = myDBconnection.cursor()
        sample_info_list = []
        cursor.execute("SELECT * FROM viacord.sampleinfo")
        mycursor = cursor.fetchall()
        if mycursor is None:
            Configuration.closeDBconnection(cursor, myDBconnection)
            return "No data found."
        else:
            for row in mycursor:
                sample_info = SampleInfo(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9],
                                         row[10], row[11], row[12], row[13], row[14], row[15], row[16], row[17], row[18],
                                         row[19], row[20], row[21])
                sample_info_list.append(sample_info)
            Configuration.closeDBconnection(cursor, myDBconnection)
            return sample_info_list


# GET SAMPLE BY ID
    @staticmethod
    def getSampleByID(id):
        myDBconnection = Configuration.openDBconnection()
        cursor = myDBconnection.cursor()
        cursor.execute("SELECT * FROM viacord.sampleinfo WHERE id = %s", [id])
        mycursor = cursor.fetchone()
        if mycursor is None:
            Configuration.closeDBconnection(cursor, myDBconnection)
            return "No data found."
        else:
            Configuration.closeDBconnection(cursor, myDBconnection)
            return SampleInfo(mycursor[0], mycursor[1], mycursor[2], mycursor[3], mycursor[4], mycursor[5], mycursor[6],
                              mycursor[7], mycursor[8], mycursor[9], mycursor[10], mycursor[11], mycursor[12], mycursor[13],
                              mycursor[14], mycursor[15], mycursor[16], mycursor[17], mycursor[18], mycursor[19],
                              mycursor[20], mycursor[21])


# GET SAMPLE BY SAMPLE ID
    @staticmethod
    def getSampleBySampleID(sampleId):
        myDBconnection = Configuration.openDBconnection()
        cursor = myDBconnection.cursor()
        cursor.execute("SELECT * FROM viacord.sampleinfo WHERE sampleId = %s", [sampleId])
        mycursor = cursor.fetchone()
        if mycursor is None:
            Configuration.closeDBconnection(cursor, myDBconnection)
            return "No data found."
        else:
            Configuration.closeDBconnection(cursor, myDBconnection)
            return SampleInfo(mycursor[0], mycursor[1], mycursor[2], mycursor[3], mycursor[4], mycursor[5], mycursor[6],
                              mycursor[7], mycursor[8], mycursor[9], mycursor[10], mycursor[11], mycursor[12], mycursor[13],
                              mycursor[14], mycursor[15], mycursor[16], mycursor[17], mycursor[18], mycursor[19],
                              mycursor[20], mycursor[21])


# GET SAMPLES BY DATE - SAMPLE INFO
    @staticmethod
    def getAllSampleInfoByDate(labelingDate):
        myDBconnection = Configuration.openDBconnection()
        cursor = myDBconnection.cursor()
        sample_info_list = []
        cursor.execute("SELECT * FROM viacord.sampleinfo WHERE labelingDate = %s", [labelingDate])
        mycursor = cursor.fetchall()
        cursor.close()
        if mycursor is None:
            Configuration.closeDBconnection(cursor, myDBconnection)
            return "No data found."
        else:
            for row in mycursor:
                sample_info = SampleInfo(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9],
                                         row[10], row[11], row[12], row[13], row[14], row[15], row[16], row[17], row[18],
                                         row[19], row[20], row[21])
                sample_info_list.append(sample_info)
            Configuration.closeDBconnection(cursor, myDBconnection)
            return sample_info_list


# EDIT SAMPLE - PROCESSED SAMPLES
    @staticmethod
    def updateSampleInfo(sampleInfo, bufferVolume):
        myDBconnection = Configuration.openDBconnection()
        cursor = myDBconnection.cursor()
        sInfo = json.loads(sampleInfo)
        sInfo["bufferVolume"] = bufferVolume
        print("The Sample ID i'm going to edit is:", sInfo["sampleId"], "and the new Buffer Volume is:", bufferVolume)
        mySqlQuery = """UPDATE viacord.sampleinfo SET initialWeight = %s, labelingDate = %s, 
        bufferVolume = %s WHERE sampleID = %s;"""
        myData = (sInfo["initialWeight"], sInfo["labelingDate"], bufferVolume, sInfo["sampleId"])
        cursor.execute(mySqlQuery, myData)
        Configuration.closeDBconnection(cursor, myDBconnection)
        return sInfo
