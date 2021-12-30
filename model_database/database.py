from database_config import *

#Create Legacy application model, database table and fields
class LegacyApp(db.Model):
    #Create a table
    __tablename__ = 'tbl_legacy_application_list'
    id = db.Column(db.Integer, nullable=False, primary_key=True, unique=True)
    url = db.Column(db.String(128), nullable=False )
    description = db.Column(db.String(128), nullable=False )
    app_name = db.Column(db.String(128), nullable=False )
    pwd = db.relationship('PasswordList', back_populates="parent" , lazy='joined')

        #Add new legacy application to PMS    
    def add_new_legacy_app(_app_name,_url,_description):
        new_legacy_app = LegacyApp(app_name=_app_name,description=_description,url=_url)
        db.session.add(new_legacy_app)  # create a new record
        db.session.commit()  # commit changes to session
        return new_legacy_app

#Create Password  model, database table and fields
class PasswordList(db.Model):
    #Create a table
    __tablename__ = 'tbl_app_password_list'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    password = db.Column(db.String(128))
    user_id = db.Column(db.Integer())
    #created_date = db.Column(db.DateTime(), default=datetime.utcnow)
    app_id = db.Column(db.Integer(), db.ForeignKey('tbl_legacy_application_list.id'))
    parent = db.relationship("LegacyApp", back_populates="pwd")


#Create User  model, databaUserListse table and fields
class UserList(db.Model):
    #Create a table
    __tablename__ = 'tbl_users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32))
    password = db.Column(db.String(128))
    email = db.Column(db.String(128))
    role = db.Column(db.String(20))
    passwordCriteraStatus = db.Column(db.Integer())

     #Check the email address in the database when your trying to login to system
    def check_login(_email):
        user = UserList.query.filter_by(email=_email).first()
        if user is None:
            return False
        else:
            return user

     #Create dummy admin User
    def add_new_admin_user(_username,_password,_email,_role,_passwordCriteraStatus):
        new_user = UserList(role=_role,username=_username,password=_password,email=_email,passwordCriteraStatus=_passwordCriteraStatus)
        db.session.add(new_user)  # add new password to database session
        db.session.commit()  # commit changes to session
        return new_user

        
    #Create new user and save in database
    def add_new_user(_username,_password,_email,_role,_passwordCriteraStatus):
        new_user = UserList(role=_role,username=_username,password=_password,email=_email,passwordCriteraStatus=_passwordCriteraStatus)
        db.session.add(new_user)  # add new password to database session
        db.session.commit()  # commit changes to session
        return new_user

    #Filter user by ADMIN role
    def get_user_by_id(_id):
        userIsExist = UserList.query.filter_by(id=_id, role="ADMIN").first()
        if userIsExist is None:
            return False
        else:
            return True


class UserSchema(Schema):
    username = fields.String(required=True)
    password = fields.String(required=True)
    email = fields.String(required=True)


class LoginUserSchema(Schema):
    password = fields.String(required=True)
    email = fields.String(required=True)

class LegacyAppSchema(Schema):
    url = fields.String(required=True)
    description = fields.String(required=True)
    app_name = fields.String(required=True)

db.create_all()