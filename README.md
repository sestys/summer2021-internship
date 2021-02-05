# Wolt Summer 2021 Backend Internship
Solution to preliminary backend engineering assignment by Matej Sestak.
This app is written in Python and uses Flask framework.
I decided not to use any database.

This code was developed and tested on Ubuntu 20.04, please use same system to run it.

## Install
Create virtualenv and activate:
```
python3 -m venv wolt_intern
. venv/bin/activate
```

Install dependencies:
```
pip install -r requirements.txt
```

## Run
Run following commands in a terminal:
```
export FLASK_APP=app
export FLASK_ENV=development
flask run
```
Then open [http://127.0.0.1:5000/discovery](http://127.0.0.1:5000/discovery) in any browser.

## Test
To run tests, run pytest in the project root directory:
```
pytest
```