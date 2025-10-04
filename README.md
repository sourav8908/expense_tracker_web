# Personal Expense Tracker

A simple web-based personal expense tracker built with **Flask** and **MySQL**.

---

## Features

- Add new expenses with amount, date, note, and category  
- View all expenses in a table  
- Update/edit existing expenses  
- Delete expenses  
- Data saved in a MySQL database  
- Basic validation and error handling  
- Simple and clean Bootstrap-based UI

---

## Technology Stack

- Python 3.x  
- Flask (Web framework)  
- Flask-MySQLdb (MySQL connector)  
- WTForms (Form validation)  
- MySQL (Database)  
- Bootstrap 5 (UI styling)

---

## Setup and Installation

### Prerequisites

- Python 3.x installed  
- MySQL Server installed and running

### Step 1: Clone or download the repo

```bash
git clone https://github.com/sourav8908/expense_tracker_web.git
cd expense_tracker_web


Step 2: (Optional but recommended) Create and activate a virtual environment
python -m venv venv
.\venv\Scripts\activate


Step 3: Install dependencies
pip install flask flask-mysqldb flask-wtf wtforms


Step 4: Setup MySQL database
1. Open MySQL command line or Workbench and run the following commands:
CREATE DATABASE expense_tracker_db;

CREATE USER 'expense_user'@'localhost' IDENTIFIED BY 'password123';

GRANT ALL PRIVILEGES ON expense_tracker_db.* TO 'expense_user'@'localhost';

FLUSH PRIVILEGES;

USE expense_tracker_db;

CREATE TABLE expenses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    amount DECIMAL(10,2) NOT NULL,
    expense_date DATE NOT NULL,
    note VARCHAR(255),
    category VARCHAR(50)
);


Step 5: Configure the app
Open app.py and update the MySQL configuration to match your setup:

app.config['MYSQL_USER'] = 'expense_user'
app.config['MYSQL_PASSWORD'] = 'password123'
app.config['MYSQL_DB'] = 'expense_tracker_db'



Step 6: Run the Flask application
In PowerShell, set the environment variable and start the app:

$env:FLASK_APP = "app.py"
python -m flask run


Access the application
Open your browser and go to:

http://127.0.0.1:5000/


Usage
• Click Add Expense to add new expenses
• Use Edit button to update expenses
• Use Delete button to remove expenses
• Data is saved persistently in MySQL database

Assumptions and Design Notes
• Single-user application (no authentication)
• Categories are predefined but can be customized
• Basic validation on input fields using WTForms
• Ul built with Bootstrap for simplicity and responsiveness

License
This project is open source and free to use.









