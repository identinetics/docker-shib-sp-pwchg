from ldap import LDAPConfiguration
import os


class Config(LDAPConfiguration):
    """Configuration object.
    
        Configuration is loaded from the process environment.
        
        Look into LDAPConfiguration for parameters.
             
    """
    LDAP_ROOT_PASSWORD = os.environ['ROOTPW'] if 'ROOTPW' in os.environ else 'changeit'
    SLAPDPORT = os.environ['SLAPDPORT'] if 'SLAPDPORT' in os.environ else '8389'
    SLAPDHOST = os.environ['SLAPDHOST'] if 'SLAPDHOST' in os.environ else '10.1.1.6'
    ROOTDN = os.environ['ROOTDN'] if 'ROOTDN' in os.environ else 'dc=at'
    ADMINDN = os.environ['ADMINDN'] if 'ADMINDN' in os.environ else 'cn=admin,dc=at'
    USERNAME_IN = os.environ['USERNAME_IN'] if 'USERNAME_IN' in os.environ else 'HTTP_UID'
    USER_TO_DN = os.environ['USER_TO_DN'] if 'USER_TO_DN' in os.environ else '{}'


    def __init__(self):
        super(Config,self).__init__()
