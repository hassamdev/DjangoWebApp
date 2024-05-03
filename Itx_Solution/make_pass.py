
import requests,json


# The URL you want to send the POST request to
url = 'http://127.0.0.1:8000/add/app-user'

data = {
    "f_name":"hassam",
    "l_name":"ghori",
    "email":"hassamghori722@gmail.com",
    "cell_no":1234,
    "gender":"MALE",
    "birth_date":"1-2-2000",
    "password":"PASSWORD",
}
# Create a session
session = requests.Session()

session.headers.update({"auth-app":'itx_solution'})
response = session.get(url,json=data)

# Check the response status code
if response.status_code == 200:
    body = json.loads(response.text)
    print(body)
    print(type(body['flag']))
else:
    print('Failed to fetch the CSRF token. Status code:', response.status_code)


















