#Add dependencies to seperate file and we simply import it with all attributes
from flask_sqlalchemy import model
from database_config import *


# Import user defined libs
from model_database.database import LegacyApp
from model_database.database import UserList
from model_database.database import PasswordList
from model_database.database import UserSchema
from model_database.database import LoginUserSchema
from module_password.password import Password


app.config['SECRET_KEY'] = os.environ['secretkey']

# Access controll module
# Without having a proper JWT authentication token cannot access to API
def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None
        if 'x-access-tokens' in request.headers:
            token = request.headers['x-access-tokens']
        if not token:
            return jsonify({
                'Error Meesage': "A Valid token is missing!"
            }), 401
        try:

            token = jwt.decode(token, app.config['SECRET_KEY'],algorithms=["HS256"])
            return f(*args,  **kwargs)
        
        except (jwt.exceptions.InvalidSignatureError, jwt.InvalidTokenError, exceptions.BadRequest):
            return jsonify({
                'Error Meesage': "Your token is expired! Please login in again"
            }), 401

    return decorator
# Access controll module end



##Input validation
def required_params(schema):
    def decorator(fn):
 
        @wraps(fn)
        def wrapper(*args, **kwargs):
            try:
                schema.load(request.get_json())
            except ValidationError as err:
                error = {
                    "status": "error",
                    "messages": err.messages
                }
                return jsonify(error), 400
            return fn(*args, **kwargs)
 
        return wrapper
    return decorator
##Input validation




# User registration module
@app.route('/signup', methods=['POST'])
#This is for input validation
#This annotation represent validation
@required_params(UserSchema())
def register():
    try:
        request_data = request.get_json()
        username = str(request_data['username'])
        password = str(request_data['password'])
        email = request_data['email']
        role = "USER"
        pwdcriteastatus = 1
        #Check this email address is already exist or not
        user = UserList.check_login(email)
        if user:
            error_message = "This email address is already registered!"
            return jsonify({
                'Error Meesage': error_message
            }), 401
        else:
            hibp_result = Password.check_hibp(password)
            is_complexity, complexity_result_msg = Password.check_complexity(
                password)
            hash_result = Password.hash_pwd(password)

            if is_complexity is False:
                return jsonify(Process='ERROR!', Process_Message=complexity_result_msg)

            elif hibp_result is True:
                return jsonify(Process='ERROR!', Process_Message='This password is already in HIBP Database.')

            else:
                # return jsonify(Process='SUCESS!', Process_Message='Good Password!')
                # return jsonify(hash_result)
                response = UserList.add_new_user(
                    username, hash_result, email, role, pwdcriteastatus)
                return jsonify({"Message": "Succesfuly saved"}), 201


    except (KeyError, exceptions.BadRequest):
        return jsonify(Process='ERROR!', Process_Message='Your token is expired! Please login in again.')
# User registration module en



# User login module Start
@app.route('/login', methods=['POST'])
@required_params(LoginUserSchema())
def login():
    request_data = request.get_json()
    email = request_data['email']
    entered_password = request_data['password']
    # Do password verification
    user = UserList.check_login(email)
    try:
        if user:
            current_pwd = user.password
            user_password_status = user.passwordCriteraStatus
            if user_password_status == 0:
                Message = "System adminstartor recently change the password policy. Please update the password!"
            else:
                Message = "Your password meet complexity."

            if Password.verify_password(entered_password, current_pwd):
                login_session['id'] = user.id
                expiration_date = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
                token = jwt.encode({"exp": expiration_date},app.config['SECRET_KEY'], algorithm="HS256")
                #print(type(token))
                #print(token)
                #login_session['logged_in'] = True
                return jsonify({
                    'Token': token,
                    'Message': Message
                }), 200
            else:
                error_message = "Your username or password is invalid"
                return jsonify({
                    'Error Meesage': error_message
                }), 401

        else:
            error_message = "Your username or password is invalid"
            return jsonify({
                'Error Meesage': error_message
            }), 401
    except (KeyError, exceptions.BadRequest):
        return jsonify(Process='ERROR!', Process_Message='Something went wrong! Please login in again')
# User login module end





# Run server
if __name__ == '__main__':
    app.run(debug=True)  
    