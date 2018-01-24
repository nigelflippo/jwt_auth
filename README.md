# FLASK TOKEN AUTH

- Setup
```bash
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
$ createdb jwt_auth
$ flask db init
$ flask db migrate
$ flask db upgrade
$ export FLASK_APP=api.py
```

- JWT
```bash
>>> import os
>>> os.urandom(24)
$ export SECRET_KEY='code generated above'
```

- Use HTTPIE to test routes