from flask import Flask, render_template, flash, redirect, url_for, request, abort
import jwt
import datetime
import forms, db


app = Flask(__name__)
app.config['SECRET_KEY'] = 'D3O5W8iIsiGjoLck1KQ3VzjCypqvT7oV'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/user/<id>')
def user(id):
    user_info = db.get_user_info(id)
    if user_info is None:
        abort(404, "User not found")
    else:   
        return render_template('user.html', user_info=user_info)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = forms.RegisterForm()
    if form.validate_on_submit():

        result = db.create_new_user(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            password=form.password.data,
            age=form.age.data,
            biography=form.biography.data,
            city=form.city.data)

        if result is not None:
            flash(f"New user successfully registered. User Id is '{result}'")
            return redirect(url_for('login', id=result))
        
    
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    request.content_type

    form = forms.LoginForm()

    if form.validate_on_submit():
        result = db.verify_user(form.id.data, form.password.data)

        if result:
            return redirect(url_for('user', id=form.id.data))
        else:
            flash("Authentication failed! Try again") 

    user_id = request.args.get('id')
    form.id.data = user_id

    return render_template('login.html', form=form)


#service funstions section

def encone_token(user_id):
    payload = {
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=600),
        'iat': datetime.datetime.utcnow(),
        'sub': user_id
    }
    return jwt.encode(
        payload,
        app.config.get('SECRET_KEY'),
        algorithm='HS256'
    )


#API functions section

#login user
@app.route('/api/v1/login', methods=['POST'])
def api_login():

    post_data = request.get_json()
    user_id = post_data.get("id")
    password = post_data.get("password")

    if user_id  is None:
        abort(400, "'id' parameter is required")

    if password  is None:
        abort(400, "'password' parameter is required")


    result = db.verify_user(user_id, password)

    if result:
        token = encone_token(user_id)
        return {"token": encone_token(user_id)}
    else:
        abort(400, "authentication failed")

#register new user
@app.route('/api/v1/user/register', methods=['POST'])
def api_register():

    post_data = request.get_json()
    
    first_name = post_data.get("first_name")
    last_name = post_data.get("last_name")
    password = post_data.get("password")
    age = post_data.get("age")
    city = post_data.get("city")
    biography = post_data.get("biography")

    if first_name is None:
        abort(400, "'first_name' parameter is required") 

    if last_name is None:
        abort(400, "'last_name' parameter is required") 

    if password is None:
        abort(400, "'password' parameter is required") 

    result = db.create_new_user(first_name, last_name, password, age, city, biography)

    if result:
        return {"user_id": result}
    else:
        abort(500) 

#get user's data
@app.route('/api/v1/user/<id>', methods=['GET'])
def api_user(id):
    user_info = db.get_user_info(id)
    if user_info is None:
        abort(404, "User not found")
    else:   
        return user_info
   

#search users by name
@app.route('/api/v1/user/search', methods=['GET'])
def api_search():

    first_name = request.args.get("first_name")
    last_name = request.args.get("last_name")

    if first_name is None and last_name is None:
        abort(400, "at least one of the parameters 'first_name' or 'last_name' is required")


    result = db.search_user(first_name, last_name)

    return result

if __name__ == "__main__":
    app.run(port=8000, debug=True)