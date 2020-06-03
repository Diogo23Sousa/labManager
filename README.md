# ViaCordBuffer
The purpose of this application is to facilitate the work related to the management of the sample information in the current laboratory protocol for the ViaCord stem cell cryopreservation process.

# Initializing the webApp 
1. You will need to install: Python3 and the needed packages by using the command in the main folder:

                                          pip install -r requirements.txt
                                          
2. Download mySQL and run the DDL file and then import the dataTables in mySQL that are inside the folder ../dataSets/

3. Running the FLASK server - Run the following command inside the folder ../backEnd/viacord/main:
  
                                          python app.py
 
 
4. Install NPM and Angular CLI and install the dependencies
     
                                          npm install -g @angular/cli
                                          npm install

5. Running the client (LH:4200) (Typescrypt | Angular 8+) - Inside the folder ../front-end/via-cord-angular - run the following command:
  
                                          npm start --open

6. Open the browser and type the following url: http://localhost:4200/
