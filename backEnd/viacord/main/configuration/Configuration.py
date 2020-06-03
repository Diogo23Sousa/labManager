import mysql.connector
from flask import Blueprint

# BLUEPRINT (project_configuration)
project_configuration = Blueprint('project_configuration', __name__, template_folder='templates')


class Configuration:
    def __init__(self):
        self = self

# Connect to my DB
    @staticmethod
    def openDBconnection():
        dbConnection = mysql.connector.connect(host="localhost", user="root", passwd="rootroot", database="viacord")
        dbConnection.connect()
        return dbConnection

# Close my DB connection
    @staticmethod
    def closeDBconnection(cursor, dbConnection):
        cursor.close()
        dbConnection.commit()
        dbConnection.close()