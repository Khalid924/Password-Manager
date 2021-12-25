#Add dependencies to seperate file and we simply import it with all attributes
from database_config import *


# Import user defined libs
from model_database.database import LegacyApp
from model_database.database import UserList
from model_database.database import PasswordList



# Run server
if __name__ == '__main__':
    app.run(debug=True)  
    