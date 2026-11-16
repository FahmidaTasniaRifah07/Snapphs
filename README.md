# Snapphs
### An Automated Personalized Birthday Bot
Making birthday wishes personal, effortless, automatic and delivered right on time.

## Overview
Snapphs is a Python based birthday automation project designed to send personalized birthday emails automatically even when the user is offline.
It combines Python, SQLite, GitHub API integration and GitHub Actions to manage birthday records and automate email delivery.

## Key Features
- **Birthday Management:** Add, view, update and delete birthday records.
- **Personalized Emails:** Send customized birthday wishes using individual messages.
- **Automated Scheduling:** Automatically check for birthdays and trigger email delivery.
- **Database Synchronization:** Synchronize local database changes with private GitHub storage.
- **Duplicate Prevention:** Prevent repeated birthday emails within the same year.
- **Persistent Storage:** Store birthday information using SQLite.

## How It Works
Snapphs consists of three main components:
### 1. Local System - `Snapphs.py`
- Manages birthday records.
- Supports adding, viewing, updating and deleting information.
- Uses SQLite for local database management.
- Retrieves and synchronizes database changes with private GitHub storage.

### 2. Cloud Storage - Private GitHub Repository
- Stores the SQLite database (`snapphs.db`).
- Keeps birthday records separate from the public source code.
- Provides database access to the automation workflow through authorized credentials.

### 3. Cloud Automation - `BB_V3.py`
- Runs automatically through GitHub Actions.
- Retrieves the latest database.
- Checks for birthdays.
- Sends personalized emails through Gmail SMTP.
- Updates the database after successful email delivery.
- Synchronizes the updated database with private GitHub storage.

### Automation Flow
```text
Local System
    |
    | Add / Update / Delete Records
    v
Private GitHub Database
    |
    | Download Database
    v
GitHub Actions
    |
    v
Birthday Detection
    |
    | Birthday Found
    v
Personalized Email Delivery
    |
    v
Update Database
    |
    | Upload Updated Database
    v
Private GitHub Database
```

## Technologies Used
| Technology | Purpose |
|---|---|
| Python | Core programming language |
| SQLite | Birthday data storage |
| GitHub API | Database synchronization |
| GitHub Actions | Cloud-based automation |
| Gmail SMTP | Email delivery |
| Python-dotenv | Environment variable management |
| Requests | HTTP requests to GitHub API |

## Dependencies
Snapphs uses the following external Python packages:
```text
python-dotenv==1.2.4
requests
```
The following modules are included with Python and do not require separate installation:
- `base64`
- `os`
- `sys`
- `sqlite3`
- `smtplib`
- `email.message`
- `datetime`
- `zoneinfo`
**Python requirement:** Python 3.9 or newer.
Install the external dependencies using:
```bash
pip install -r requirements.txt
```

## Project Structure
```text
Snapphs/
│
├── .github/
│   └── workflows/
│       ├── birthday-automation.yml
│       └── python.yml
│
├── .gitignore
├── BB_V3.py
├── README.md
├── Snapphs.py
└── requirements.txt
```
The database (`snapphs.db`) is maintained separately in a private GitHub repository and is not included in the public source-code repository.

## Setup and Configuration
To run your own instance of Snapphs:
1. Clone this repository:
```bash
git clone https://github.com/FahmidaTasniaRifah07/Snapphs.git
```
2. Navigate to the project directory:
```bash
cd Snapphs
```
3. Install the required dependencies:
```bash
pip install -r requirements.txt
```
4. Configure your own environment variables and credentials.
5. Create your own private GitHub repository to store your birthday database.
6. Configure the required GitHub Actions secrets and repository settings.
7. Run the local application:
```bash
python Snapphs.py
```
**Note:** The complete automated system requires additional configuration including Gmail credentials, GitHub API access, a private database repository and GitHub Actions secrets. The required environment variable names must match those used in the Python scripts.

## Privacy and Security
Snapphs separates its public source code from private user data.
- The source code is available in the public repository.
- Birthday records are stored in a separate private repository.
- Gmail credentials and GitHub access tokens are managed through environment variables and GitHub Actions secrets.
- Sensitive files, including `.env` and local database files should not be committed to the public repository.
- Anyone setting up their own instance must configure their own credentials and database.
**Cloning the public repository does not provide access to the original private database or its stored information.**

## Developer
**Fahmida Tasnia Rifah**  
Aeronautical Engineering Student

Snapphs was developed as a hands-on project to explore Python programming, database management, API integration and cloud-based automation.




