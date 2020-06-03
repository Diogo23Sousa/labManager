import json
from flask import Blueprint
from viacord.main.models.ProcessedSample import ProcessedSample
from viacord.main.configuration.Configuration import Configuration

# BLUEPRINT (processed_samples_repository)
processed_samples_repository = Blueprint('processed_samples_repository', __name__, template_folder='templates')


class ProcessedSamplesRepository:
    def __init__(self):
        self = self


# GET ALL - PROCESSED SAMPLES
    @staticmethod
    def getAllProcessedSamples():
        myDBconnection = Configuration.openDBconnection()
        processed_sample_list = []
        cursor = myDBconnection.cursor()
        cursor.execute("SELECT * FROM viacord.processedsamples")
        mycursor = cursor.fetchall()
        if mycursor is None:
            Configuration.closeDBconnection(cursor, myDBconnection)
            return "No data found."
        else:
            for row in mycursor:
                processed_sample = ProcessedSample(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
                processed_sample_list.append(processed_sample)
            Configuration.closeDBconnection(cursor, myDBconnection)
            return processed_sample_list


# GET SAMPLE BY ID - PROCESSED SAMPLES
    @staticmethod
    def getSampleByID(id):
        myDBconnection = Configuration.openDBconnection()
        cursor = myDBconnection.cursor()
        cursor.execute("SELECT * FROM viacord.processedsamples WHERE id = %s", [id])
        mycursor = cursor.fetchone()
        if mycursor is None:
            Configuration.closeDBconnection(cursor, myDBconnection)
            return "No data found."
        else:
            Configuration.closeDBconnection(cursor, myDBconnection)
            return ProcessedSample(mycursor[0], mycursor[1], mycursor[2], mycursor[3], mycursor[4], mycursor[5],
                                   mycursor[6])


# GET SAMPLE BY SAMPLE ID - PROCESSED SAMPLES
    @staticmethod
    def getSampleBySampleID(sampleId):
        myDBconnection = Configuration.openDBconnection()
        cursor = myDBconnection.cursor()
        cursor.execute("SELECT * FROM viacord.processedsamples WHERE sampleId = %s", [sampleId])
        mycursor = cursor.fetchone()
        if mycursor is None:
            Configuration.closeDBconnection(cursor, myDBconnection)
            return "No data found."
        else:
            Configuration.closeDBconnection(cursor, myDBconnection)
            return ProcessedSample(mycursor[0], mycursor[1], mycursor[2], mycursor[3], mycursor[4], mycursor[5], mycursor[6])


# GET SAMPLES BY DATE - PROCESSED SAMPLES
    @staticmethod
    def getAllProcessedSamplesByDate(sampleDate):
        myDBconnection = Configuration.openDBconnection()
        cursor = myDBconnection.cursor()
        processed_sample_list = []
        cursor.execute("SELECT * FROM viacord.processedsamples WHERE sampleDate = %s", [sampleDate])
        mycursor = cursor.fetchall()
        if mycursor is None:
            Configuration.closeDBconnection(cursor, myDBconnection)
            return "No data found."
        else:
            for row in mycursor:
                processed_sample = ProcessedSample(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
                processed_sample_list.append(processed_sample)
            Configuration.closeDBconnection(cursor, myDBconnection)
            return processed_sample_list


# NEW SAMPLE - PROCESSED SAMPLES
    @staticmethod
    def newProcessedSample(processedSample):
        myDBconnection = Configuration.openDBconnection()
        cursor = myDBconnection.cursor()
        pSample = json.loads(processedSample)
        print("The Sample ID i'm going to add is:", pSample["sampleId"], "isInitialWeight know?", pSample["isWeightKnown"],
              "the Weight is: ", pSample["initialWeight"], "therefore the volume is:", pSample["bufferVolume"])

        mySqlQuery = """INSERT INTO viacord.processedsamples (id, sampleID, isInitialWeightKnown, initialWeight, 
        sampleDate, comments, bufferVolume) VALUES (%s, %s, %s, %s, %s, %s, %s) """
        myData = (pSample["id"],
                  pSample["sampleId"],
                  pSample["isWeightKnown"],
                  pSample["initialWeight"],
                  pSample["sampleDate"],
                  pSample["comments"],
                  pSample["bufferVolume"])
        cursor.execute(mySqlQuery, myData)
        Configuration.closeDBconnection(cursor, myDBconnection)
        return "New sample was created."


# EDIT SAMPLE - PROCESSED SAMPLES
    @staticmethod
    def editProcessedSample(processedSample):
        myDBconnection = Configuration.openDBconnection()
        cursor = myDBconnection.cursor()
        pSample = json.loads(processedSample)
        print("The Sample ID i'm going to edit is:", pSample["sampleId"])
        print("The new sample Weight is: ", pSample["initialWeight"])
        mySqlQuery = """UPDATE viacord.processedsamples SET initialWeight = %s, sampleDate = %s, comments = %s, 
        bufferVolume = %s WHERE sampleId = %s;"""
        myData = (pSample["initialWeight"], pSample["sampleDate"], pSample["comments"],
                  pSample["bufferVolume"], pSample["sampleId"])
        cursor.execute(mySqlQuery, myData)
        Configuration.closeDBconnection(cursor, myDBconnection)
        return "Processed sample was updated."

# DELETE SAMPLE - PROCESSED SAMPLES
    @staticmethod
    def deleteProcessedSampleBySampleId(sampleId):
        myDBconnection = Configuration.openDBconnection()
        cursor = myDBconnection.cursor()
        cursor.execute("DELETE FROM viacord.processedsamples WHERE sampleId = %s", [sampleId])
        Configuration.closeDBconnection(cursor, myDBconnection)
        return "Sample was deleted."

# DELETE ALL - PROCESSED SAMPLES
    @staticmethod
    def deleteAllProcessedSamples():
        myDBconnection = Configuration.openDBconnection()
        cursor = myDBconnection.cursor()
        cursor.execute("DELETE FROM viacord.processedsamples")
        Configuration.closeDBconnection(cursor, myDBconnection)

