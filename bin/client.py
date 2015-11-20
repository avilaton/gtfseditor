import requests
import cookielib

class Client(object):

    def __init__(self, name, url):
        self.name = name
        self.url = url
        self.api = url + '/api'

        self.cookie_file = './cookie-' + self.name

        self.cj = cookielib.LWPCookieJar(self.cookie_file)
        try:
            self.cj.load()
        except:
            pass

        self.session = requests.Session()
        self.session.cookies = self.cj

    def login(self, email, password):
        self.session.get(self.url + '/auth/login')
        self.session.post(self.url + '/auth/login', data={"email": email, "password": password})

    def getList(self, resource):
        return self.session.get(self.api + resource).json()

    def create(self, resource, payload):
        return self.session.post(self.api + resource, json=payload)

    def save_cj(self):
        self.cj.save(ignore_discard=True)