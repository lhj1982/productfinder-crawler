import base64
import requests


def get_oscar_token(oscar_data):
    client_id = oscar_data.get('client_id')
    client_secret = oscar_data.get('client_secret')
    authorization = f'{client_id}:{client_secret}'.encode()
    encode = str(base64.b64encode(authorization), 'utf-8')
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': f'Basic {encode}'
    }
    data = {
        'grant_type': 'client_credentials',
        'scope': oscar_data.get('scopes')
    }
    response = requests.post(oscar_data.get('oscar_issuer'), headers=headers, data=data)
    if response.status_code == 200:
        return response.json().get('access_token')
    else:
        raise ValueError('get oscar token error')
