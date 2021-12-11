from flask import Flask
from client import *
from middleware.auth import AuthorizationMiddle


app=Flask(__name__)
app.wsgi_app=AuthorizationMiddle(app.wsgi_app)

users={
    '1':{'name': 'admin', 'money':100500},
    '2':{'name':'semen', 'money':0},
    '3':{'name':'olya', 'money':1200000000}
}

@app.route('/')
def index():
    print('im from index')
    return 'ind'

@app.route('/get-money')
def get_money():
    user_id=requests.headers('auth_middleware_user')
    return json.dumos({'user_id':user_id, 'money':users.get(user_id)['money']})

if __name__=='__main__':
    app.run(host='127.0.0.1', port='5001')