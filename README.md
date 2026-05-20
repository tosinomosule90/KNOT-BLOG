# Flask Company App

A simple Flask web application for user registration and login.

## Features

- User registration with password validation
- User login/logout
- Dashboard for authenticated users
- SQLite database for data storage

## Project Structure

```
special/
├── app/
│   ├── __init__.py      # App factory
│   ├── extension.py     # Flask extensions
│   ├── model.py         # WTForms
│   ├── table.py         # Database models
│   ├── view.py          # Routes and views
│   ├── static/          # CSS, JS, images
│   └── templates/       # HTML templates
├── app.py               # Application entry point
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## Installation

1. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

2. Run the application:

   ```bash
   python app.py
   ```

3. Open http://localhost:5000 in your browser

## Usage

- Visit the root URL to register a new account
- Use the login page to sign in
- Access the dashboard after authentication
