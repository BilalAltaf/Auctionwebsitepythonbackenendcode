__author__ = 'Bilal'
import re
class validator():
    @staticmethod
    def isValidEmail(email):
        if re.match(r'^[a-zA-Z0-9._-]+@[a-zA-Z0-9-]+\.[a-zA-Z.]{2,5}$', email):
            return True
        else:
            return False
    @staticmethod
    def isValidName(name):
        if re.match(r'^[a-zA-Z ,.-]+$', name):
            return True
        else:
            return False
    @staticmethod
    def isValidUserName(name):
        if re.match(r'^[a-zA-Z0-9]+([._]?[a-zA-Z0-9]+)*$', name):
            return True
        else:
            return False
    @staticmethod
    def isValidPassword(password):
        if len(password) > 5:
            return True
        else:
            return False
    @staticmethod
    def isValidAddress(address):
        if re.match(r'^[a-zA-Z0-9\s,-/.]*$', address):
            return True
        else:
            return False
    @staticmethod
    def isValidDecimalwithTwoDecimal(DecimalNo):
        if re.match(r'^[0-9]+(\.[0-9]{1,2})?$', DecimalNo):
            return True
        else:
            return False
    @staticmethod
    def isValidText(description):
        if re.match(r'^[a-zA-Z0-9\s,-/.]*$', description):
            return True
        else:
            return False
    @staticmethod
    def isValidId(Auctionid):
        if re.match('^[0-9]+',Auctionid):
            return True
        else:
            return False