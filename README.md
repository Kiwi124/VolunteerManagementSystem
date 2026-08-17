UrbanConnect Volunteer Management System

*******************************************
This is a university project. This application is not meant for a production environment. Please carefully read this to setup your local environment correctly to prevent any issues.                    
*******************************************

Setup Instructions
===================

Prerequisites
-------------
- Python 3.13
- MySQL Server (running locally, with a root/admin account you can create databases with)
- Git
- Node.js v24.19.0

Installing Node.js
===================
https://nodejs.org/en/download

Recommended (Windows):
```
# Download and install Chocolatey:
powershell -c "irm https://community.chocolatey.org/install.ps1|iex"

# Download and install Node.js:
choco install nodejs --version="24.19.0"

# Verify the Node.js version:
node -v # Should print "v24.19.0".

# Verify npm version:
npm -v # Should print "11.17.0".
```

Recommended (Mac/Linux):
```
# Download and install nvm:
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.6/install.sh | bash

# in lieu of restarting the shell
\. "$HOME/.nvm/nvm.sh"

# Download and install Node.js:
nvm install 24

# Verify the Node.js version:
node -v # Should print "v24.19.0".

# Verify npm version:
npm -v # Should print "11.17.0".
```

1. Clone the repository
------------------------
```
git clone <repo-url>
cd VolunteerManagementSystem
```

2. Create and activate a virtual environment
---------------------------------------------
```
python -m venv venv
```
Windows (PowerShell):
```
.\venv\Scripts\Activate.ps1
```
Mac/Linux:
```
source venv/bin/activate
```

3. Install dependencies
------------------------
```
pip install -r requirements.txt
```

4. Create the MySQL database
------------------------------
Log into MySQL and create an empty database:
```
CREATE DATABASE vmsdb;
```

Then open `volunteer_management_system/settings.py` and update the `DATABASES` block with
your own local MySQL username/password if they differ from the default `root` / `root`:
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'vmsdb',
        'USER': 'root',      # your local DB user
        'PASSWORD': 'root',  # your local DB password
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}
```

5. Load the database
----------------------
A SQL dump (`vms_dump.sql`) is provided in the repo with the current schema and reference
data. Import it into the empty database created above:
```
mysql -u root -p vmsdb < vms_dump.sql
```

If no dump is provided or you'd rather start from a clean database, run migrations instead:
```
python manage.py migrate
```

7. Run the development server
--------------------------------
In a terminal run: 
```
labb dev
```

In a new terminal run:
```
python manage.py runserver
```
The app will be available at http://127.0.0.1:8000/

Troubleshooting
----------------
- **`django.db.utils.OperationalError` / can't connect to MySQL server**: confirm MySQL is
  running locally and the `USER`/`PASSWORD`/`PORT` in `settings.py` match your local setup.
- **`pip install` fails on `mysqlclient`**: this package needs MySQL's C build tools/headers.
  On Windows, installing MySQL Server/Workbench usually covers this; on Mac/Linux you may
  need `brew install mysql` or `apt install default-libmysqlclient-dev` first.
- **Import of `vms_dump.sql` fails**: make sure the target database (`vmsdb`) exists and is
  empty before importing, and that you're using the same MySQL user that owns/can write to it.
