import os
from ldap3 import Server,Connection, ALL, LDIF, MODIFY_REPLACE
from ldap3.core.exceptions import LDAPBindError

class LDAPUserSearchFoundTooManyUsersException(Exception):
    pass

class LDAPUserSearchFoundNoUserException(Exception):
    pass

class LDAPConfiguration(object):
    """Configuration object.

         Loads the config from the process environment.

         Users should know what to put into most of these, except:

         USERNAME_IN :
             The apache (request) environment variable where the username (dn) is found.
         USER_TO_DN: 
             Simple way to expand the username into a dn. Like "uid={}, dc=example, dc=com"

     """
    LDAP_ROOT_PASSWORD = os.environ['ROOTPW'] if 'ROOTPW' in os.environ else 'changeit'
    SLAPDPORT = os.environ['SLAPDPORT'] if 'SLAPDPORT' in os.environ else '8389'
    SLAPDHOST = os.environ['SLAPDHOST'] if 'SLAPDHOST' in os.environ else 'localhost'
    ROOTDN = os.environ['ROOTDN'] if 'ROOTDN' in os.environ else 'dc=at'
    ADMINDN = os.environ['ADMINDN'] if 'ADMINDN' in os.environ else 'cn=admin,dc=at'
    USERNAME_IN = os.environ['USERNAME_IN'] if 'USERNAME_IN' in os.environ else 'HTTP_UID'
    USER_TO_DN = os.environ['USER_TO_DN'] if 'USER_TO_DN' in os.environ else '{}'


    def __init__(self):
        self.SLAPDHOST = self.SLAPDHOST.rstrip()
        self.server = ":".join([self.SLAPDHOST, self.SLAPDPORT])


class LDAPConnection(object):

    def __init__(self,config):
        """Abstraction for the LDAP Connection.

        Args:
            config: The configuration Object for this connection.
        """
        self.config = config
        self.server = Server(config.server, get_info=ALL)
        self.connection = Connection(self.server, config.ADMINDN, config.LDAP_ROOT_PASSWORD,
                                    auto_bind=True,
                                    raise_exceptions=True)

        self.connection.search(self.config.ROOTDN, '(objectclass=*)')
        return


    def search_user(self,filter):
        entries = self.search(filter)
        if len(entries) > 1:
            raise LDAPUserSearchFoundTooManyUsersException
        if len(entries) < 1:
            raise LDAPUserSearchFoundNoUserException
        user_dn = entries[0].entry_dn
        return user_dn

    def search(self,filter):
        self.connection.search(self.config.ROOTDN, str(filter))
        return self.connection.entries


    def change_password(self,userdn,new_password):
        #print ("changing pw: userdn={} new_password={}".format(userdn, new_password))
        self.connection.modify(userdn, {'userPassword': [(MODIFY_REPLACE, [new_password])]})
        return

    def dump_testuser(self):
        self.connection.search(self.config.ROOTDN, '(objectclass=*)')
        return self.connection.entries

    def test_userdn_password(self,userdn,password):
        try:
            test_connection = Connection(self.server,userdn,password,auto_bind=True)
        except LDAPBindError as e:
            """ looks a little bit ugly but:
            http://stackoverflow.com/questions/28575359/how-to-bind-authenticate-a-user-with-ldap3-in-python3
            (which doesn't work well also?)
            """
            if str(e).endswith('invalidCredentials'):
                return False
            else:
                raise e
        return True


class LDAPFilterItem(object):
    def __init__(self,attrib,value):
        self.attrib = attrib
        self.value=value

    def __str__(self):
        return "({}={})".format(self.attrib,self.value)


class LDAPFilter(object):
    def __init__(self):
        self.filters = []

    def add(self,filter):
        self.filters.append(filter)

    def add_filter(self,attrib,value):
        f = LDAPFilterItem(attrib,value)
        self.filters.append(f)

    def __str__(self):
        f_str = "".join([str(x) for x in self.filters])
        return "(&{})".format(f_str)





