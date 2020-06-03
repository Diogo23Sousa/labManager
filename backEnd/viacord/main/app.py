from flask import Flask
from flask_cors import CORS

from viacord.main.business.ProcessedSamplesBusiness import processed_samples_business
from viacord.main.configuration.Configuration import project_configuration
from viacord.main.configuration.EmailSender import email_sender
from viacord.main.controllers.SampleInfoController import sample_info_controller
from viacord.main.controllers.ProcessedSamplesController import processed_samples_controller
from viacord.main.repositories.SampleInfoRepository import sample_info_repository
from viacord.main.repositories.ProcessedSamplesRepository import processed_samples_repository

print("--------------------------------------------APPLICATION IS STARTING--------------------------------------------")

# FLASK CONFIGURATION
app = Flask(__name__)
CORS(app)

# BLUEPRINT REGISTER BEFORE APPLICATION RUNNING
app.register_blueprint(project_configuration)
app.register_blueprint(email_sender)

# MY REPOSITORIES
app.register_blueprint(sample_info_repository)
app.register_blueprint(processed_samples_repository)

# MY BUSINESS
app.register_blueprint(processed_samples_business)

# MY CONTROLLERS
app.register_blueprint(sample_info_controller)
app.register_blueprint(processed_samples_controller)

if __name__ == '__main__':
    app.run()