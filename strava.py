import json
from google.appengine.api import urlfetch
import logging

STRAVA_API = 'https://www.strava.com/api/v3/athletes/1044822/activities'
STRAVA_OAUTH_API = 'https://www.strava.com/oauth/'
API_ACCESS_TOKEN = '35a85aa2ac6f7f8d617c9e5e9814255a7f8fa10b'
API_REFRESH_TOKEN = '0539c68fa767a8b3be67062a0cda50519679a3e5'
API_SECRET = '64d606fdc30b9bc5395c5ad4007330b6578e50e0'
API_CLIENT_ID = '30291'
ATHLETE_ID = '1044822'

def run_data():
    stravaUrl = STRAVA_API
    # stravaUrl += ATHLETE_ID + '/stats/'
    stravaUrl += '?access_token=' + API_ACCESS_TOKEN

    jsonRaw = urlfetch.fetch(stravaUrl)
    jsonObject = json.loads(jsonRaw.content)

    logging.info(stravaUrl)
    logging.info(jsonObject)

    return []

# def strava_oauth_call():
#     stravaUrl = STRAVA_OAUTH_API + 'authorize/'
#     stravaUrl += '?client_id=' + API_CLIENT_ID
#     stravaUrl += '&scope=activity:read_all'
#     stravaUrl += '&response_type=code'
#     stravaUrl += '&redirect_uri=https://patdugan.me'
#     return result.content

def strava_oauth_refresh():
    stravaUrl = STRAVA_OAUTH_API + 'token'
    stravaUrl += '?client_id=' + API_CLIENT_ID
    stravaUrl += '&client_secret=' + API_SECRET
    stravaUrl += '&code=35a85aa2ac6f7f8d617c9e5e9814255a7f8fa10b'
    stravaUrl += '&grant_type=authorization_code'

    logging.info(stravaUrl)
    result = urlfetch.fetch(stravaUrl)

    return result.content

# 'https://www.strava.com/oauth/authorize?client_id=30291&scope=activity:read_all&response_type=code&redirect_uri=http://patdugan.me&approval_prompt=force'
# 'https://www.strava.com/oauth/token?client_id=30291&client_secret=64d606fdc30b9bc5395c5ad4007330b6578e50e0&code=37ffdbf59ef65a98665c86d3c587840a462b2a53&grant_type=authorization_code'
