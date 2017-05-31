import re
from ldap3.utils.dn import escape_attribute_value

class PasswordTooShortException(Exception):
    pass


class Password(object):
    MIN_PASSWORD_LENGTH = 8

    def __init__(self,password=None):
        self.password = None
        if password is not None:
            self.set_password(password)
        return

    def set_password(self,password,checks=True):
        if checks:
            self.pw_check(password)
        self.password = EscapedPart(password)
        return

    def pw_check(self,password):
        self._pw_has_min_length(password)
        return

    def _pw_has_min_length(self, password):
        if len(password) < self.MIN_PASSWORD_LENGTH:
            raise PasswordTooShortException

    def __str__(self):
        return str(self.password)


class EscapedPart(object):
    def __init__(self,txt):
        self.txt = txt
        if self.txt is None:
            self.escaped = None
        else:
            self.escaped = escape_attribute_value(txt)

    def __str__(self):
        return self.escaped



