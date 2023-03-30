import requests

server = "http://127.0.0.1:5000/"
session = requests.Session()
# login

data = {"username": "iakovos", "password": "1234"}
try:
    username = ''
    result = session.post(server + "login", json = data, timeout = 5, auth=('username', 'password'))
    print(result.status_code, result.json())
    if result.status_code == 200:
        print("ok")
    else:
        print("Αποτυχία σύνδεσης στο python-quiz -if")
except:
    print("Αποτυχία σύνδεσης στο python-quiz -try")

# send score
data = {"score": 0.8}
try:
    result = session.post(server + "end", json = data, timeout = 5)
    print(result.status_code, result.json())
    if result.status_code == 200:
        print("ok")
    else:
        print("Αποτυχία σύνδεσης στο python-quiz -send-if")
except:
    print("Αποτυχία σύνδεσης στο python-quiz -send-try")

