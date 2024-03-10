# extract.py
# extract recently played data from spotify API
import requests
import json

def get_access_token(client_id, client_secret):
    '''
    authenticate and get access token
    '''
    AUTH_URL = 'https://accounts.spotify.com/api/token'
    CLIENT_ID = client_id
    CLIENT_SECERT = client_secret

    auth_response = requests.post(AUTH_URL,
        {
        'grant_type': 'client_credentials',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECERT 
        }
    )

    #convert response to JSON and grab auth token
    auth_response_data = auth_response.json()
    access_token = auth_response_data['access_token']

    return access_token

def get_request_results(client_id, client_secret, base_url, show_id):
    '''
    fetch episode results from api for specific show and output to json
    '''
    access_token = get_access_token(client_id, client_secret)
    headers = {'Authorization': 'Bearer {token}'.format(token=access_token)}
    BASE_URL = base_url
    SHOW_ID = show_id
    episodes_country = '/episodes?market=US'

    r = requests.get(BASE_URL+SHOW_ID+episodes_country, headers = headers)
    data = r.json()

    #now output to json file
    with open("episodes.json", "w") as outfile:
        json.dump(data, outfile, indent = 4)

    return data

def main(args):
    if len(args) != 5:
        raise SystemExit(f'Usage: {sys.argv[0]} ' 'need 4 parameters')
    get_request_results(args[1],args[2], args[3], args[4])
