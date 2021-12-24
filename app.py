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

