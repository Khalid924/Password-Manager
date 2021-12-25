from database_config import *


# Import user defined libs
from password_module.password import Password
from password_module.pwd_complex_edit import PasswordComplexityEdit
from db_models.pms_models import PasswordList
from db_models.pms_models import LegacyApp
from db_models.pms_models import UserList
from db_models.pms_models import UserSchema
from db_models.pms_models import PasswordSchema
from db_models.pms_models import LegacyAppSchema
from db_models.pms_models import LoginUserSchema
from db_models.pms_models import UpdatePasswordSchema


app.config['SECRET_KEY'] = os.environ[current_env+'_secretkey']

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