# event-manager-app

## Introduction

This is a Django project that is used to manage events.
The installed app define api urls used to:
- create/update/delete events, update and delete are allowed only to event owner
- list all events
- list own events
- register/unregister to event


## Setup

To run this project, it's recommended to use a virtual environment to isolate the project dependencies.

### Prerequisites

1. Python 3.x installed on your system.
2. [Optional] `virtualenv` package installed globally (you can install it using `pip install virtualenv`).

### Setting up a Virtual Environment (Optional)

1. Open your terminal or command prompt and navigate to the project's root directory.

2. Create a virtual environment by running the following command:
   ```
   python3 -m venv virtshell
   ```

3. Activate the virtual environment:
   ```
   source env/bin/activate
   ```

### Installing Dependencies

Once you have activated the virtual environment, install the required dependencies from the `requirements.txt` file:
```
pip install -r requirements.txt
```

### Project commands

1. The project use sqlite so a db.sqlite3 file will be created launching migrations:
```
python manage.py migrate
```

## Additional Information

#### Postman collection
The project have also a postman collection, and an associated environment, to test the api.
Use the request **Set Token (POST)** to get an access_token; this one is set as environment variable and is automatically used to authenticate next requests.
In order to retrieve the access_token you have to set **_username_** and **_password_** in collection variables.

Create a "simple" user using signup page `/manager/signup/`, or create and admin user using shell command: 
```
python manage.py createsuperuser
```

