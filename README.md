# FLASK TOKEN AUTH

## Setup
- Install python3, virtualenv

```bash
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
$ createdb jwt_auth
$ export FLASK_APP=api.py
$ flask db init
$ flask db migrate
$ flask db upgrade
```

- JWT
```bash
>>> import os
>>> os.urandom(24)
$ export SECRET_KEY='code generated above'
```

- Use HTTPIE to test routes