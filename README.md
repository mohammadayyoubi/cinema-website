# 🎬 Cinema Website

Welcome to the Cinema Website project, a web application built using Flask that allows users to create accounts, book tickets, and view a list of movies. Admin users have additional capabilities to manage movies and user accounts.

## 📋 Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## 🌟 Features

- **User Registration and Authentication:** 
  - Users can create and manage their own accounts.
  - Secure login and registration process.
  
- **Movie Listings:**
  - Browse a list of movies with detailed information.
  - Search and filter movies by various criteria.
  
- **Ticket Booking:**
  - Book tickets for available movies.
  - View booking history.
  
- **User Account Management:**
  - Users can edit their own account details.
  
- **Admin Panel:**
  - Admin users can add, delete, and edit movies.
  - Manage user accounts and permissions.

## 🛠️ Installation

### Prerequisites

- Python 3.6+
- pip (Python package installer)
- Virtual environment tool (optional but recommended)

### Steps

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/cinema-website.git
   cd cinema-website
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment:**
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install the required packages:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Set up the environment variables:**
   - Create a `.env` file in the root directory and add the following:
     ```env
     FLASK_APP=app.py
     FLASK_ENV=development
     SECRET_KEY=your_secret_key
     ```

6. **Initialize the database:**
   - first in python script make sure you fill the app.config correctly to be contain the right (username / password / host / name of database) in your laptop...
   - second:
   ```bash
   flask db init
   flask db migrate
   flask db upgrade

8. **insert the data of rooms & seats:**
   - you can find .txt file named "db seats + room" it contains set of commands to insert the data... Please copy paste them in workbench to be inserted.
   - soon we will fix it to be automatically inserted with opn :)
   ```

## 🚀 Usage

1. **Run the application:**
   ```bash
   flask run
   ```

2. **Open your web browser and go to:**
   ```
   http://127.0.0.1:5000/
   ```

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Commit your changes (`git commit -m 'Add some feature'`).
5. Push to the branch (`git push origin feature-branch`).
6. Open a pull request.
