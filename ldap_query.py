import ldap
import re 

class Query():
    
    def __init__(self):
        self._email = None
        self._id = None
        self._name = None

    @property
    def email(self):
        return self._email
    
    @property
    def name(self):
        return self._name
    
    @property
    def id(self):
        return self._id
    
    @id.setter
    def id(self, num):
        #print(num)
        num_length = len(num)
        if num_length < 7 or num_length > 8:
            raise IdLengthError(num)
        if re.match("^[0-9]+$", num) == True:
            raise IdNonNumberError(num)
        self._id = num
    
    def find_details(self):
        if self._id == None:
            raise IdIsNoneError

        try:
            l = ldap.initialize("ldap://ldap.soton.ac.uk")
            l.protocol_version = ldap.VERSION3
        except ldap.LDAPError as e:
            print(e)

        baseDN = "OU=User,DC=soton,DC=ac,DC=uk"
        searchScope = ldap.SCOPE_SUBTREE
        retrieveAttributes = ["givenName", "employeeNumber", "mail"]
        searchFilter = "employeeNumber={}".format(self._id)

        try:
            ldap_result_id = l.search(baseDN, searchScope, searchFilter, retrieveAttributes)
            while 1:
                result_type, result_data = l.result(ldap_result_id, 0)
                if result_data == []:
                    break
                else:
                    if result_type == ldap.RES_SEARCH_ENTRY:
                        for tup in result_data:
                            self._name = tup[1]["givenName"][0].decode("utf-8")
                            self._email = tup[1]["mail"][0].decode("utf-8") 
        except ldap.LDAPError as e:
            print("Could not obtain information on that person")
            #print(e)



class QueryError(Exception):
    pass

class IdLengthError(QueryError):
    def __init__(self, expression):
        self.expression = expression
        self.message = "The inputted id value must be 7 or 8 characters long"

class IdNonNumberError(QueryError):
    def __init__(self, expression):
        self.expression = expression
        self.message = "The inputted id value must only contain numbers"

class IdIsNoneError(QueryError):
    def __init__(self):
        self.expression = None
        self.message = "The inputted id is none."

