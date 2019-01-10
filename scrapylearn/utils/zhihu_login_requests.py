
import requests

from http import cookiejar

# 会话对象让你能够跨请求保持某些参数。它也会在同一个 Session 实例发出的所有请求之间保持 cookie
session = requests.session()
session.cookies = cookiejar.LWPCookieJar(filename="cookies.txt")
try:
    session.cookies.load(ignore_discard=True)
except:
    print("no cookies")
def is_login():
    pass

def get_mark():
    pass


def login():

    session.cookies.save()
    pass
