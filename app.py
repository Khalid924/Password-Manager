#Add dependencies to seperate file and we simply import it with all attributes
from database_config import *


# Import user defined libs
from model_database.database import LegacyApp
from model_database.database import UserList
from model_database.database import PasswordList
from model_database.database import UserSchema
from model_password.password import Password

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
            hash_result = Password.(password)

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




# Run server
if __name__ == '__main__':
    app.run(debug=True)  
    