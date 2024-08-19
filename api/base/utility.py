import re

regex_username = re.compile(r'^[a-zA-Z_0-9]\w{2,19}$')
def check_username(username):
    if re.fullmatch(regex_username, username):
        return True 
    else:
        return False