from database_config import *
from json import load
import pyhibp
from pyhibp import pwnedpasswords as pw
import bcrypt
import os
import string

class Password:
    @staticmethod
    def check_hibp(password):
        # Required: A descriptive user agent must be set describing the application consuming
        #   the HIBP API
        pyhibp.set_user_agent(ua="PMS-User")

        # Check a password to see if it has been disclosed in a public breach corpus
        resp = pw.is_password_breached(password=password)
        if resp:
            #print("Password breached!")
            #print("This password was used {0} time(s) before.".format(resp))
            return True
        # Get data classes in the HIBP system
        resp = pyhibp.get_data_classes()

        # Get all breach information
        resp = pyhibp.get_all_breaches()

        # Get a single breach
        resp = pyhibp.get_single_breach(breach_name="Adobe")

        # An API key is required for calls which search by email address
        #   (so get_pastes/get_account_breaches)
        # See <https://haveibeenpwned.com/API/Key>
        HIBP_API_KEY = None

        if HIBP_API_KEY:
            # Set the API key prior to using the functions which require it.
            pyhibp.set_api_key(key=HIBP_API_KEY)

            # Get pastes affecting a given email address
            resp = pyhibp.get_pastes(email_address="test@example.com")

            # Get breaches that affect a given account
            resp = pyhibp.get_account_breaches(account="test@example.com", truncate_response=True)