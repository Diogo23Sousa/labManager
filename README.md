
# Sample Management WebApp

This application is designed to streamline the management of sample information, providing an efficient and user-friendly interface for handling related tasks.

---

## Getting Started

### Prerequisites

To set up and run this application, you need the following installed on your system:

- **Python 3**
- **MySQL**
- **Node.js**
- **Angular CLI**

---

## Setup Instructions

### 1. Install Python Packages

Navigate to the main folder of the project and install the required Python packages by running:

```bash
pip install -r requirements.txt
```

### 2. Set Up the Database

1. Install **MySQL** and create the necessary database structure.
2. Run the provided **DDL file**.
3. Import the data tables located in the folder:  
   ```
   ../dataSets/
   ```

### 3. Run the Flask Server

Navigate to the backend folder and start the Flask server by running the following command:

```bash
cd ../backEnd/viacord/main
python app.py
```

The backend will start and listen for requests.

### 4. Install Angular Dependencies

Navigate to the frontend folder and install the required dependencies:

```bash
npm install -g @angular/cli
npm install
```

### 5. Run the Angular Client

Navigate to the Angular frontend folder and start the client server:

```bash
cd ../front-end/via-cord-angular
npm start --open
```

This will open the application in your default browser at `http://localhost:4200/`.

---

## Accessing the Application

After following the steps above:

1. Open your browser and navigate to:  
   ```
   http://localhost:4200/
   ```
2. The application is now ready to use.

---
