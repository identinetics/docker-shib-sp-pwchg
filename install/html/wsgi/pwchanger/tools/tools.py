import random
import logging
import string

log = logging.getLogger('werkzeug')


def randomword(length):
    """Just a word with somewhat random letters.
   
    Args:
        length: Length of the word
    
    Returns:
        A word of (non-cyrypto-secure) random lowercase letters.
    """
    return ''.join(random.choice(string.ascii_lowercase) for i in range(length))


class Log(object):
    def info(self,msg):
        log.info(msg)

    def error(self,msg):
        log.error(msg)

    def logline(request, msg=""):
        l = "{}:{} {} {}".format(request.environ['REMOTE_ADDR'], request.environ['REMOTE_PORT'], request.host_url, msg)
        log.info(l)
