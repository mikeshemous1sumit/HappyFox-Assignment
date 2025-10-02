
## Directory Structure

```
gmail_rule_engine/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── README.md
├── .env
├── rules.json
├── src/
│   ├── config.py
│   ├── fetch_emails.py
│   ├── process_emails.py
│   ├── actions/
│   ├── db/
│   ├── gmail/
│   ├── rules/
│   └── utils/
├── tests/
│   ├── test_actions.py
│   ├── test_db.py
│   ├── test_gmail.py
│   └── test_rules.py
```

- `src/` contains all source code modules.
- `tests/` contains unit tests.
- `rules.json` defines email rules.
- `.env` stores environment variables.
- Docker files enable easy setup and deployment.

---

## Environment Variables (.env)

You can configure paths and database settings using a `.env` file in the project root.  
Example `.env`:

```
GMAIL_CREDENTIALS_PATH=./gmail_credentials.json
RULES_JSON_PATH=./rules.json
DB_URL=postgresql+psycopg2://myuser:mypassword@localhost:5432/gmail_rule_engine
```

The project uses [python-dotenv](https://pypi.org/project/python-dotenv/) to automatically load these variables.


## How to Run

### Option 1: Using Docker (Recommended) 

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/gmail-rule-engine-assignment.git
   cd gmail-rule-engine-assignment/gmail_rule_engine
   ```

2. **Place your `gmail_credentials.json` file in the project directory.**
   - See instructions below for how to obtain this file.

3. **Build and start the app and PostgreSQL database:**
   ```bash
   docker-compose up --build
   ```

4. **Run scripts or tests inside the container:**
   ```bash
   docker-compose run app python src/fetch_emails.py
   docker-compose run app python src/process_emails.py
   docker-compose run app pytest tests/
   ```

---

### Option 2: Manual Setup (Without Docker)

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/gmail-rule-engine-assignment.git
   cd gmail-rule-engine-assignment/gmail_rule_engine
   ```

2. **Create and activate a Python virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up PostgreSQL:**
   - Install PostgreSQL and start the service.
   - Create a database and user matching your `src/config.py` settings (or update `DB_URL` accordingly).

5. **Obtain Gmail API credentials:**
   - Go to [Google Cloud Console](https://console.cloud.google.com/).
   - Create a new project (or use an existing one).
   - Enable the Gmail API for your project.
   - Go to "APIs & Services" > "Credentials".
   - Click "Create Credentials" > "OAuth client ID".
   - Download the `credentials.json` file and place it in the project directory (as specified in `config.py`).

6. **Run the scripts:**
   ```bash
   python src/fetch_emails.py
   python src/process_emails.py
   ```

7. **Run tests:**
   ```bash
   pytest tests/
   ```

---


## How to Obtain `gmail_credentials.json`

- Go to [Google Cloud Console](https://console.cloud.google.com/).
- Create a new project or select an existing one.
- Enable the Gmail API for your project.
- Go to "APIs & Services" > "Credentials".
- Click "Create Credentials" > "OAuth client ID".
- Download the `credentials.json` file and place it in your project directory.

**Note:**  
Do **not** commit or share your `credentials.json` file publicly.

---

## About `token.json`

When you run the Gmail API scripts for the first time, you will be prompted to authorize access in your browser/console. After successful authorization, a file named `token.json` will be generated automatically in your project directory. This file securely stores your access and refresh tokens.

**Purpose:**
- `token.json` allows the app to reuse your credentials for future runs, so you do not have to authorize every time.
- If `token.json` is present and valid, the app will use it to authenticate silently.
- If you delete or invalidate `token.json`, you will be prompted to authorize again.

**Do not share or commit your `token.json` file publicly.**
