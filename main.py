from flask import Flask, render_template, flash, redirect, url_for, request, abort, Response
import forms, db, cache, taran, rabbit, reqs
import jwt
import datetime
import logging 

app = Flask(__name__)
app.config['SECRET_KEY'] = 'D3O5W8iIsiGjoLck1KQ3VzjCypqvT7oV'
app.config["JSON_AS_ASCII"] = False
app.config["JSONIFY_MIMETYPE"] = "application/json; charset=utf-8"

LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(name) -30s %(funcName) '
              '-35s %(lineno) -5d: %(message)s')
LOGGER = logging.getLogger(__name__)

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
            flash("Authorization failed! Try again") 

    user_id = request.args.get('id')
    form.id.data = user_id

    return render_template('login.html', form=form)


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
        return {"token": token}
    else:
        abort(400, "Authorization failed")

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

#set user's friend
@app.route('/api/v1/friend/set/<user_id>', methods=['PUT'])
def put_user_friend(user_id):

    if 'Authorization' in request.headers:
        token = request.headers.get('Authorization')
        auth_data = decode_token(token)

        if 'user_id' in auth_data:
            current_user_id = auth_data['user_id']
            result = db.add_friend(current_user_id, user_id)

            if result == True:
                return {"success": True}
            elif result == 1062:
                return {"success": False, "message": "Users are friends already"}
            elif result == 1406:
                return {"success": False, "message": "User id is invalid"}
            elif result == 1452:
                return {"success": False, "message": "User is not defined"}
            else:
                abort(400, "Bad request")
        else:
            abort(403, "Authorization token is invalid")

    return {"success": False, "message": "Authorization token is required"}

#create new post for currnet user
@app.route('/api/v1/post/create', methods=['POST'])
def create_post():

    if 'Authorization' in request.headers:
        token = request.headers.get('Authorization')
        auth_data = decode_token(token)

        if 'user_id' not in auth_data:
            abort(403, "Authorization token is invalid")
        current_user_id = auth_data['user_id']    

        post_data = request.get_json(silent=True)
        if post_data is None:
            abort(400, "Bad request")
        
        text = post_data.get("text")
        if text is None:
            abort(400, "Post text is required")
  
        #(post_id, friends) = db.add_post_friends(current_user_id, text)
        #if post_id is None:
        #    return {"success": False, "message": "Error creating new post"}
        #else:
            #cache.clear_cache(current_user_id)
        rabbit.add_post(current_user_id, text)
        return Response({"success": True}, status=202, mimetype='application/json')
        #    return post_id
    else:
            abort(403, "Authorization token is invalid")

#get user feed
@app.route('/api/v1/post/feed', methods=['GET'])
def get_feed():


    try:
        offset = int(request.args.get("offset"))
    except:
        offset = 0

    try:
        limit = int(request.args.get("limit"))
    except:
        limit = 10    

    current_user_id = authorization_user(request)

    if current_user_id is None:
        abort(403, "Authorization token is invalid")
         
    feed = cache.get_feed_chached(current_user_id)
    if feed is None:
        return {"success": False, "message": "Error getting user's feed"}
    else:
        return feed[offset:offset+limit]



#post user dialog
@app.route('/api/v1/dialog/<user_id>/send', methods=['POST'])
def send_dialog(user_id):

    post_data = request.get_json()
    text = post_data.get("text")
    
    if text  is None:
        abort(400, "'text' body parameter is required")

    current_user_id = authorization_user(request)

    if current_user_id is None:
        abort(403, "Authorization token is invalid")

    #dialog = db.send_dialog(current_user_id, user_id, text)
    dialog = taran.send_dialog(current_user_id, user_id, text)
    if dialog is None:
        return {"success": False, "message": "Error sending text"}
    else:
        return dialog

#post dialog list
@app.route('/api/v1/dialog/<user_id>/list', methods=['GET'])
def list_dialog(user_id):

    current_user_id = authorization_user(request)

    if current_user_id is None:
        abort(403, "Authorization token is invalid")

    dialog = db.list_dialog(current_user_id, user_id)
    if dialog is None:
        return {"success": False, "message": "Error geting dialogs"}
    else:
        return dialog



#post user dialog V2
@app.route('/api/v2/dialog/<user_id>/send', methods=['POST'])
def send_dialog_v2(user_id):

    LOGGER.info('Receive request /api/v2/dialog/<user_id>/send.  user_id = %s', user_id)

    post_data = request.get_json()
    text = post_data.get("text")
    
    if text  is None:
        abort(400, "'text' body parameter is required")

    current_user_id = authorization_user(request)

    if current_user_id is None:
        abort(403, "Authorization token is invalid")

    #dialog = db.send_dialog(current_user_id, user_id, text)
    #dialog = taran.send_dialog(current_user_id, user_id, text)
    dialog = reqs.send_dialog(current_user_id, user_id, text)
    if dialog is None:
        return {"success": False, "message": "Error sending text"}
    else:
        return dialog

#get dialog list
@app.route('/api/v2/dialog/<user_id>/list', methods=['GET'])
def list_dialog_v2(user_id):

    LOGGER.info('Receive request /api/v2/dialog/<user_id>/list.  user_id = %s', user_id)

    current_user_id = authorization_user(request)

    if current_user_id is None:

        LOGGER.warning('Authorization token is invalid.  user_id = %s', user_id)

        abort(403, "Authorization token is invalid")

    #dialog = db.list_dialog(current_user_id, user_id)
    dialog = reqs.list_dialog(current_user_id, user_id)
    if dialog is None:
        return {"success": False, "message": "Error geting dialogs"}
    else:
        return dialog

            

#service funstions section

def authorization_user(request):
    user_id = None

    if 'Authorization' in request.headers:
        token = request.headers.get('Authorization')
        auth_data = decode_token(token)


        if 'user_id' in auth_data:
            user_id = auth_data['user_id']

    return user_id     



def encone_token(user_id):
    """
    Decodes the auth token
    :param user_id:
    :return: string
    """
    try:
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=3600),
            'iat': datetime.datetime.utcnow(),
            'sub': user_id
        }
        return jwt.encode(
            payload,
            app.config.get('SECRET_KEY'),
            algorithm='HS256'
        )
    except Exception as e:
        return e

def decode_token(auth_token):
    """
    Decodes the auth token
    :param auth_token:
    :return: integer|string
    """
    try:
        payload = jwt.decode(auth_token, app.config.get('SECRET_KEY'), algorithms=["HS256"])
        return {'user_id':payload['sub']}
    except jwt.ExpiredSignatureError:
        return {'error':'Signature expired. Please log in again.'}
    except jwt.InvalidTokenError:
        return {'error': 'Invalid token. Please log in again.'}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8001, debug=True)