# flask_demo
demo web-server for social network project
## features
- Create and preview users profile
- Search users profile by name
- Authorization with JWT
- Front interface and API 
## API
api specification in `openapi.yaml`
- `POST /login` - sign in for registered user
- `POST /user/register` - new user registration
- `GET /user/<id>` - get user's profile
- `GET /user/search` - search user
for more information run postman collection `flask.postman_collection.json`

## install instructions 
- install and create a new virtual environment
``` shell
pip install virtualenv
virtualenv venv
```
- install necessary packeges
``` shell
pip install flask
pip install Flask-WTF
pip install pyjwt
pip install datetime
pip install uuid
pip install mysql-connector-python
```
- install and configure MySQL
<br/> https://www.mysql.com/downloads/
<br/> the default settings:
```
user: root
pass: password
db: flask
```
- run `python create_db.py` to create users table in flask db

- run `python main.py` to start flask_demo (127.0.0.1:8000)